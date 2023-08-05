# -*- coding: utf-8 -*-
"""
oathldap_srv.hotp_validator.handler - the request handler
"""

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

import crypt
import logging
import json
from base64 import b32decode

# from cryptography
import cryptography.hazmat.backends
import cryptography.hazmat.primitives.twofactor.hotp
import cryptography.hazmat.primitives.hashes

# PyNaCL
import nacl.exceptions

# from pynacl
from nacl.pwhash.argon2id import verify as argon2_verify

# from jwcrypto
try:
    from jwcrypto.jwe import JWE
except ImportError:
    JWE = JWK = None

# from ldap0 package
import ldap0
import ldap0.functions
from ldap0 import LDAPError
from ldap0.controls.simple import RelaxRulesControl
from ldap0.controls.libldap import AssertionControl
from ldap0.functions import is_expired

# local modules
from slapdsock.handler import SlapdSockHandler, SlapdSockHandlerError
from slapdsock.message import (
    CONTINUE_RESPONSE,
    InternalErrorResponse,
    SuccessResponse,
    InvalidCredentialsResponse,
    CompareFalseResponse,
    CompareTrueResponse,
)

#-----------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------

class DetailedResponseInfo:
    """
    message catalog with informative messages
    """
    HOTP_COUNTER_EXCEEDED = 'HOTP counter limit exceeded'
    OTP_TOKEN_EXPIRED = 'HOTP token expired'
    VERIFICATION_FAILED = (
        'user_password_compare={user_password_compare}'
        '/'
        'otp_compare={otp_compare}'
    )
    HOTP_WRONG_TOKEN_ID = 'wrong token identifier'
    ENTRY_NOT_VALID = 'not within validity period'
    OTP_TOKEN_ERROR = 'Error reading OTP token'


class SparseResponseInfo:
    """
    message catalog with no messages to avoid giving hints to attackers
    """
    HOTP_COUNTER_EXCEEDED = ''
    OTP_TOKEN_EXPIRED = ''
    VERIFICATION_FAILED = ''
    HOTP_WRONG_TOKEN_ID = ''
    ENTRY_NOT_VALID = ''
    OTP_TOKEN_ERROR = ''


class HOTPValidationHandler(SlapdSockHandler):

    """
    Handler class which validates user's password and HOTP value
    """
    infomsg = {
        False: SparseResponseInfo,
        True: DetailedResponseInfo,
    }
    token_attr_list = [
        'createTimestamp',
        'oathHOTPCounter',
        'oathHOTPParams',
        'oathSecret',
        'oathSecretTime',
        'oathTokenIdentifier',
        'oathTokenSerialNumber',
        'oathFailureCount',
    ]
    compare_assertion_type = 'oathHOTPValue'

    def __init__(self, *args, **kwargs):
        SlapdSockHandler.__init__(self, *args, **kwargs)
        # LDAP connection will be opened later on demand
        self._ldapi_conn = None

    def _check_validity_period(
            self,
            entry,
            not_before_attr,
            not_after_attr,
        ):
        """
        Check validity period, returns True if within period, else False.
        """
        not_before = entry.get(not_before_attr, [None])[0]
        not_after = entry.get(not_after_attr, [None])[0]
        return \
            (not_before is None or ldap0.functions.str2datetime(not_before) <= self.now_dt) and \
            (not_after is None or ldap0.functions.str2datetime(not_after) >= self.now_dt)
        # end of _check_validity_period()

    def _update_token_entry(
            self,
            request,
            token_dn,
            success,
            oath_hotp_next_counter,
            otp_token_entry,
        ):
        """
        update OATH token entry
        """
        mod_ctrls = None
        if success:
            # Success case
            mods = [
                # Reset failure counter
                (ldap0.MOD_REPLACE, b'oathFailureCount', [b'0']),
                # Store last login
                (ldap0.MOD_REPLACE, b'oathLastLogin', [self.now_str.encode('ascii')]),
            ]
            # let slapd assert old value <= new value
        else:
            # Update failure counter and timestamp
            mods = [
                (
                    {
                        False: ldap0.MOD_ADD,
                        True: ldap0.MOD_INCREMENT,
                    }['oathFailureCount' in otp_token_entry],
                    b'oathFailureCount',
                    [b'1']
                ),
                (ldap0.MOD_REPLACE, b'oathLastFailure', [self.now_str.encode('ascii')]),
            ]
        if oath_hotp_next_counter is not None:
            # Update HOTP counter value!
            mods.append((
                ldap0.MOD_REPLACE,
                b'oathHOTPCounter',
                [str(oath_hotp_next_counter).encode('ascii')],
            ))
            mod_ctrls = [
                AssertionControl(True, '(oathHOTPCounter<=%d)' % (oath_hotp_next_counter,)),
            ]
        # Update the token entry
        try:
            self._ldapi_conn.modify_s(
                token_dn,
                mods,
                req_ctrls=mod_ctrls,
            )
        except LDAPError as err:
            # Return unwillingToPerform to let clients fail hard
            # so they hopefully not present login form again
            self._log(
                logging.ERROR,
                'LDAPError updating token entry %r with %r: %s => unwillingToPerform',
                token_dn,
                mods,
                err,
            )
            raise SlapdSockHandlerError(
                str(err),
                log_level=logging.ERROR,
                response=InternalErrorResponse(request.msgid),
                log_vars=self.server._log_vars,
            ) from err
        else:
            self._log(
                logging.DEBUG,
                'Updated token entry %r with %r',
                token_dn,
                mods,
            )
        # end of _update_token_entry()

    def _update_pwdfailuretime(self, user_dn, user_entry, success):
        """
        update user's entry after successful login
        """
        if not success:
            # record failed login
            mods = [(ldap0.MOD_ADD, b'pwdFailureTime', [self.now_str.encode('ascii')])]
        elif 'pwdFailureTime' in user_entry:
            mods = [(ldap0.MOD_DELETE, b'pwdFailureTime', None)]
        else:
            # nothing to be done
            self._log(logging.DEBUG, 'No update of user entry %r', user_dn)
            return
        # Update the login attribute in user's entry
        try:
            self._ldapi_conn.modify_s(
                user_dn,
                mods,
                req_ctrls=[RelaxRulesControl(True)],
            )
        except LDAPError as err:
            self._log(
                logging.ERROR,
                'Error updating user entry %r with %r: %s',
                user_dn,
                mods,
                err,
            )
        else:
            self._log(logging.DEBUG, 'Updated user entry %r with %r', user_dn, mods)
        # end of _update_pwdfailuretime()

    def _check_userpassword(self, user_dn, user_entry, user_password_clear):
        """
        validate user's clear-text password against {CRYPT} password hash
        in attribute 'userPassword' of user's entry
        """
        try:
            # Strip scheme prefix {CRYPT} from password hash
            user_password_scheme, user_password_hash = user_entry['userPassword'][0][1:].split('}', 1)
        except KeyError:
            self._log(
                logging.WARN,
                'No userPassword attribute found %r',
                user_dn,
            )
            result = False
        else:
            # Compare password with local hash in attribute userPassword
            user_password_scheme = user_password_scheme.upper()
            if user_password_scheme == 'CRYPT':
                crypt_hash = crypt.crypt(
                    user_password_clear.decode('utf-8'),
                    user_password_hash.rsplit('$', 1)[0],
                )
                result = user_password_hash == crypt_hash
            elif user_password_scheme == 'ARGON2':
                try:
                    result = argon2_verify(
                        user_password_hash.encode('ascii'),
                        user_password_clear,
                    )
                except nacl.exceptions.InvalidkeyError:
                    result = False
            else:
                raise ValueError('Invalid password scheme {0!r}'.format(user_password_scheme))
        return result # _check_userpassword()

    def _get_user_entry(self, request, failure_response_class):
        """
        Read user entry
        """
        try:
            user = self._ldapi_conn.read_s(
                request.dn,
                self.server.cfg.user_filter,
                attrlist=filter(
                    None,
                    [
                        'oathHOTPToken',
                        'pwdFailureTime',
                        'userPassword',
                        self.server.cfg.user_notbefore_attr,
                        self.server.cfg.user_notafter_attr,
                    ]
                )
            )
        except ldap0.NO_SUCH_OBJECT as err:
            raise SlapdSockHandlerError(
                'User entry {!r} not found: {}'.format(
                    request.dn,
                    err,
                ),
                log_level=logging.INFO,
                response=CONTINUE_RESPONSE,
                log_vars=self.server.cfg.log_vars,
            ) from err
        except LDAPError as err:
            raise SlapdSockHandlerError(
                'Reading user entry {!r} failed: {} => {!r}'.format(
                    request.dn,
                    err,
                    failure_response_class.__name__,
                ),
                log_level=logging.WARN,
                response = failure_response_class(request.msgid),
                log_vars=self.server.cfg.log_vars,
            ) from err
        else:
            # Check whether entry was really received
            if user is None:
                raise SlapdSockHandlerError(
                    'No result reading user entry {!r} with filter {!r}'.format(
                        request.dn,
                        self.server.cfg.user_filter,
                    ),
                    log_level=logging.INFO,
                    response=CONTINUE_RESPONSE,
                    log_vars=self.server.cfg.log_vars,
                )
        return user.entry_s
        # end of _get_user_entry()

    def _get_oath_token_entry(self, request, user_entry, failure_response_class):
        """
        Read the OATH token entry for a user
        """
        # Pointer to OATH token entry, default is user entry's DN
        try:
            oath_token_dn = user_entry['oathHOTPToken'][0]
        except KeyError:
            oath_token_dn = request.dn
        # Try to read the token entry
        try:
            otp_token = self._ldapi_conn.read_s(
                oath_token_dn,
                self.server.cfg.oath_token_filter,
                attrlist=self.token_attr_list,
                cache_ttl=0, # caching disabled! (because of counter or similar)
            )
        except LDAPError as err:
            raise SlapdSockHandlerError(
                'Reading token entry {!r} failed: {} => {}'.format(
                    oath_token_dn,
                    err,
                    failure_response_class.__name__,
                ),
                log_level=logging.ERROR,
                response = failure_response_class(
                    request.msgid,
                    self.infomsg[self.server.cfg.response_info].OTP_TOKEN_ERROR,
                ),
                log_vars=self.server.cfg.log_vars,
            ) from err
        else:
            if otp_token is None:
                otp_token_entry = None
                # No available token entry => invalidCredentials
                raise SlapdSockHandlerError(
                    'Empty result reading token {!r} => {}'.format(
                        oath_token_dn,
                        failure_response_class.__name__,
                    ),
                    log_level=logging.ERROR,
                    response = failure_response_class(
                        request.msgid,
                        self.infomsg[self.server.cfg.response_info].OTP_TOKEN_ERROR,
                    ),
                    log_vars=self.server.cfg.log_vars,
                )
        return oath_token_dn, otp_token.entry_s
        # end of _get_oath_token_entry()

    def _get_oath_token_params(self, otp_token_entry):
        """
        Read OATH token parameters from referenced oathHOTPParams entry
        """
        oath_params_entry = {}
        if 'oathHOTPParams' in otp_token_entry:
            oath_params_dn = otp_token_entry['oathHOTPParams'][0]
            # Try to read the parameter entry
            try:
                oath_params = self._ldapi_conn.read_s(
                    oath_params_dn,
                    '(objectClass=oathHOTPParams)',
                    attrlist=[
                        'oathMaxUsageCount',
                        'oathHOTPLookAhead',
                        'oathOTPLength',
                        'oathSecretMaxAge',
                    ],
                    cache_ttl=self.server.cfg.oath_params_cache_ttl,
                )
            except LDAPError as err:
                self._log(
                    logging.ERROR,
                    'Error reading OATH params from %r: %s => use defaults',
                    oath_params_dn,
                    err,
                )
            else:
                if oath_params is not None:
                    oath_params_entry = oath_params.entry_s
        # Attributes from referenced parameter entry
        if not oath_params_entry:
            self._log(logging.WARN, 'No OATH params! Using defaults.')
        oath_otp_length = int(oath_params_entry.get('oathOTPLength', ['6'])[0])
        oath_hotp_lookahead = int(oath_params_entry.get('oathHOTPLookAhead', ['5'])[0])
        oath_max_usage_count = int(oath_params_entry.get('oathMaxUsageCount', ['-1'])[0])
        oath_secret_max_age = int(oath_params_entry.get('oathSecretMaxAge', ['0'])[0])
        return oath_otp_length, oath_hotp_lookahead, oath_max_usage_count, oath_secret_max_age
        # end of _get_oath_token_params()

    def _decrypt_oath_secret(self, oath_secret):
        """
        This methods extracts and decrypts the token's OATH shared
        secret from the token's LDAP entry given in argument
        :token_entry:
        """
        if not JWE or not self.server.primary_keys:
            self._log(
                logging.DEBUG,
                'no JWK keys configured => return base32-decoded oathSecret value',
            )
            return b32decode(oath_secret)
        json_s = json.loads(oath_secret)
        key_id = json_s['header']['kid']
        self._log(logging.DEBUG, 'JWE references key ID: %r', key_id)
        jwe_decrypter = JWE()
        try:
            primary_key = self.server.primary_keys[key_id]
        except KeyError:
            raise KeyError('OATH primary key with key-id %r not found' % (key_id,))
        jwe_decrypter.deserialize(oath_secret, primary_key)
        return jwe_decrypter.plaintext

    def _check_hotp(
            self,
            oath_secret,
            otp_value,
            counter,
            length=6,
            drift=0,
        ):
        """
        this function validates HOTP value
        """
        if drift < 0:
            raise ValueError('OATH counter drift must be >= 0, but was %d' % (drift,))
        otp_instance = cryptography.hazmat.primitives.twofactor.hotp.HOTP(
            self._decrypt_oath_secret(oath_secret),
            length,
            cryptography.hazmat.primitives.hashes.SHA1(),
            backend=cryptography.hazmat.backends.default_backend(),
        )
        result = None
        max_counter = counter + drift
        while counter <= max_counter:
            try:
                otp_instance.verify(otp_value, counter)
            except cryptography.hazmat.primitives.twofactor.hotp.InvalidToken:
                counter += 1
            else:
                result = counter + 1
                break
        return result
        # end of _check_hotp()

    def do_bind(self, request):
        """
        This method checks whether the request DN is a oathHOTPUser entry.
        If yes, userPassword and OATH/HOTP validation is performed.
        If no, CONTINUE is returned to let slapd handle the bind request.
        """

        # Get LDAPObject instance for local LDAPI access
        self._ldapi_conn = self.server.get_ldapi_conn()

        # Read user's entry
        user_entry = self._get_user_entry(request, InvalidCredentialsResponse)

        # Read OTP token entry
        oath_token_dn, otp_token_entry = self._get_oath_token_entry(request, user_entry, InvalidCredentialsResponse)

        # Attributes from token entry
        oath_token_identifier = otp_token_entry.get('oathTokenIdentifier', [''])[0]
        oath_token_identifier_length = len(oath_token_identifier)
        oath_token_secret_time = otp_token_entry.get(
            'oathSecretTime',
            otp_token_entry.get(
                'createTimestamp',
                [None]
            )
        )[0]

        # Try to extract/decrypt OATH counter and secret
        try:
            oath_hotp_current_counter = int(otp_token_entry['oathHOTPCounter'][0])
            oath_secret = otp_token_entry['oathSecret'][0]
        except KeyError as err:
            self._log(
                logging.ERROR,
                'Missing OATH attributes in %r: %s => %s',
                oath_token_dn,
                err,
                InvalidCredentialsResponse.__name__,
            )
            return InvalidCredentialsResponse(request.msgid)

        oath_otp_length, oath_hotp_lookahead, oath_max_usage_count, oath_secret_max_age = \
            self._get_oath_token_params(otp_token_entry)

        #-------------------------------------------------------------------
        # from here on we don't exit with a return-statement
        # and set only a result if policy checks fail

        user_password_length = len(request.cred) - oath_otp_length - oath_token_identifier_length
        # Split simple bind password and OTP part
        user_password_clear, oath_token_identifier_req, otp_value = (
            request.cred[0:user_password_length],
            request.cred[user_password_length:-oath_otp_length],
            request.cred[-oath_otp_length:]
        )
        # check the password hash
        user_password_compare = self._check_userpassword(
            request.dn,
            user_entry,
            user_password_clear
        )

        # Check OTP value
        if not otp_value:
            oath_hotp_next_counter = None
            # An empty OTP value is always considered wrong here
            self._log(
                logging.WARN,
                'Empty OTP value sent for %r',
                request.dn,
            )
            # Do not(!) exit here because we need to update
            # failure attributes later
        else:
            oath_hotp_next_counter = self._check_hotp(
                oath_secret,
                otp_value,
                oath_hotp_current_counter,
                length=oath_otp_length,
                drift=oath_hotp_lookahead,
            )
            if oath_hotp_next_counter is not None:
                oath_hotp_drift = oath_hotp_next_counter - oath_hotp_current_counter
                self._log(
                    logging.DEBUG,
                    'OTP value valid (drift %d) for %r',
                    oath_hotp_drift,
                    oath_token_dn,
                )
                # Update largest drift seen
                self.server.max_lookahead_seen = max(
                    self.server.max_lookahead_seen,
                    oath_hotp_drift
                )
            else:
                self._log(
                    logging.DEBUG,
                    'OTP value invalid for %r',
                    oath_token_dn,
                )

        otp_compare = (oath_hotp_next_counter is not None)

        # updating counter in token entry has highest priority!
        # => do it now!
        self._update_token_entry(
            request,
            oath_token_dn,
            otp_compare and oath_token_identifier.encode('utf-8') == oath_token_identifier_req,
            oath_hotp_next_counter,
            otp_token_entry,
        )

        # now do all the additional policy checks

        if not self._check_validity_period(
                user_entry,
                self.server.cfg.user_notbefore_attr,
                self.server.cfg.user_notafter_attr,
            ):
            # fail because user account validity period violated
            self._log(
                logging.WARN,
                'Validity period of %r violated! => %s',
                request.dn,
                InvalidCredentialsResponse.__name__,
            )
            response = InvalidCredentialsResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].ENTRY_NOT_VALID,
            )

        elif oath_token_identifier != oath_token_identifier_req.decode('utf-8'):
            # fail because stored and requested token identifiers different
            self._log(
                logging.WARN,
                'Token ID mismatch! oath_token_identifier=%r / oath_token_identifier_req=%r => %s',
                oath_token_identifier,
                oath_token_identifier_req,
                InvalidCredentialsResponse.__name__,
            )
            response = InvalidCredentialsResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].HOTP_WRONG_TOKEN_ID,
            )

        elif oath_hotp_current_counter > oath_max_usage_count >= 0:
            # fail because token counter exceeded
            self._log(
                logging.INFO,
                'counter limit %d exceeded for %r => %s',
                oath_max_usage_count,
                request.dn,
                InvalidCredentialsResponse.__name__,
            )
            response = InvalidCredentialsResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].HOTP_COUNTER_EXCEEDED,
            )

        elif is_expired(
                oath_token_secret_time,
                oath_secret_max_age,
                now=self.now_dt,
                disable_secs=0,
            ):
            # fail because token's shared secret too old (is expired)
            self._log(
                logging.INFO,
                (
                    'Token %r of %r is expired '
                    '(oath_token_secret_time=%r, oath_secret_max_age=%r) => %s'
                ),
                oath_token_dn,
                request.dn,
                oath_token_secret_time,
                oath_secret_max_age,
                InvalidCredentialsResponse.__name__,
            )
            response = InvalidCredentialsResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].OTP_TOKEN_EXPIRED,
            )

        elif not user_password_compare or not otp_compare:
            # user password or OTP value wrong
            self._log(
                logging.INFO,
                (
                    'Verification failed for %r (user_password_compare=%s / otp_compare=%s) => %s'
                ),
                request.dn,
                user_password_compare,
                otp_compare,
                InvalidCredentialsResponse.__name__,
            )
            response = InvalidCredentialsResponse(
                request.msgid,
                info=self.infomsg[self.server.cfg.response_info].VERIFICATION_FAILED.format(
                    user_password_compare=user_password_compare,
                    otp_compare=otp_compare,
                )
            )

        else:
            # Finally! Success!
            self._log(
                logging.INFO,
                'Validation ok for %r => response = success',
                request.dn,
            )
            response = SuccessResponse(request.msgid)

        self._update_pwdfailuretime(
            request.dn,
            user_entry,
            isinstance(response, SuccessResponse),
        )

        return response
        # end of HOTPValidationHandler.do_bind()

    def do_compare(self, request):
        """
        This method checks whether the request DN is a oathHOTPUser entry
        and whether assertion type is oathHOTPValue.
        If yes, OATH/HOTP validation is performed against assertion value.
        If no, CONTINUE is returned to let slapd handle the compare request.
        """

        if request.atype != self.compare_assertion_type:
            self._log(
                logging.DEBUG,
                'Assertion type %r does not match %r => CONTINUE',
                request.atype,
                self.compare_assertion_type,
            )
            return CONTINUE_RESPONSE

        # Get LDAPObject instance for local LDAPI access
        self._ldapi_conn = self.server.get_ldapi_conn()

        is_direct_token_cmp = (
            self.server.cfg.token_cmp_regex
            and self.server.cfg.token_cmp_regex.match(request.dn)
        )

        if is_direct_token_cmp:
            # Try to read the token entry directly
            try:
                otp_token = self._ldapi_conn.read_s(
                    request.dn,
                    self.server.cfg.oath_token_filter,
                    attrlist=self.token_attr_list,
                    cache_ttl=0, # caching disabled! (because of counter or similar)
                )
            except LDAPError as err:
                self._log(
                    logging.ERROR,
                    'Error reading token %r: %s',
                    request.dn,
                    err,
                )
                return CompareFalseResponse(
                    request.msgid,
                    self.infomsg[self.server.cfg.response_info].OTP_TOKEN_ERROR,
                )
            oath_token_dn, otp_token_entry = request.dn, otp_token.entry_s

        else:
            # Read user's entry
            user_entry = self._get_user_entry(request, InternalErrorResponse)
            # Read OTP token entry
            oath_token_dn, otp_token_entry = self._get_oath_token_entry(request, user_entry, CompareFalseResponse)

        # Attributes from token entry
        oath_token_identifier = otp_token_entry.get('oathTokenIdentifier', [''])[0]
        oath_token_secret_time = otp_token_entry.get(
            'oathSecretTime',
            otp_token_entry.get(
                'createTimestamp',
                [None]
            )
        )[0]

        # Try to extract/decrypt OATH counter and secret
        try:
            oath_hotp_current_counter = int(otp_token_entry['oathHOTPCounter'][0])
            oath_secret = otp_token_entry['oathSecret'][0]
        except KeyError as err:
            self._log(
                logging.ERROR,
                'Missing OATH attributes in %r: %s => %s',
                oath_token_dn,
                err,
                CompareFalseResponse.__name__,
            )
            return CompareFalseResponse(request.msgid)

        oath_otp_length, oath_hotp_lookahead, oath_max_usage_count, oath_secret_max_age = \
            self._get_oath_token_params(otp_token_entry)

        #-------------------------------------------------------------------
        # from here on we don't exit with a return-statement
        # and set only a result if policy checks fail

        oath_token_identifier_req, otp_value = (
            request.avalue[0:-oath_otp_length],
            request.avalue[-oath_otp_length:]
        )

        # Check OTP value
        if not otp_value:
            oath_hotp_next_counter = None
            # An empty OTP value is always considered wrong here
            self._log(
                logging.WARN,
                'Empty OTP value sent for %r',
                request.dn,
            )
            # Do not(!) exit here because we need to update
            # failure attributes later
        else:
            oath_hotp_next_counter = self._check_hotp(
                oath_secret,
                otp_value,
                oath_hotp_current_counter,
                length=oath_otp_length,
                drift=oath_hotp_lookahead,
            )
            if oath_hotp_next_counter is not None:
                oath_hotp_drift = oath_hotp_next_counter - oath_hotp_current_counter
                self._log(
                    logging.DEBUG,
                    'OTP value valid (drift %d) for %r',
                    oath_hotp_drift,
                    oath_token_dn,
                )
                # Update largest drift seen
                self.server.max_lookahead_seen = max(
                    self.server.max_lookahead_seen,
                    oath_hotp_drift
                )
            else:
                self._log(
                    logging.DEBUG,
                    'OTP value invalid for %r',
                    oath_token_dn,
                )

        otp_compare = (oath_hotp_next_counter is not None)

        # updating counter in token entry has highest priority!
        # => do it now!
        self._update_token_entry(
            request,
            oath_token_dn,
            otp_compare and oath_token_identifier.encode('utf-8') == oath_token_identifier_req,
            oath_hotp_next_counter,
            otp_token_entry,
        )

        # now do all the additional policy checks

        if not (
                is_direct_token_cmp
                or self._check_validity_period(
                    user_entry,
                    self.server.cfg.user_notbefore_attr,
                    self.server.cfg.user_notafter_attr,
                )
            ):
            # fail because user account validity period violated
            self._log(
                logging.WARN,
                'Validity period of %r violated! => %s',
                request.dn,
                CompareFalseResponse.__name__,
            )
            response = CompareFalseResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].ENTRY_NOT_VALID,
            )

        elif oath_token_identifier != oath_token_identifier_req.decode('utf-8'):
            # fail because stored and requested token identifiers different
            self._log(
                logging.WARN,
                'Token ID mismatch! oath_token_identifier=%r / oath_token_identifier_req=%r => %s',
                oath_token_identifier,
                oath_token_identifier_req,
                CompareFalseResponse.__name__,
            )
            response = CompareFalseResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].HOTP_WRONG_TOKEN_ID,
            )

        elif oath_hotp_current_counter > oath_max_usage_count >= 0:
            # fail because token counter exceeded
            self._log(
                logging.INFO,
                'counter limit %d exceeded for %r => %s',
                oath_max_usage_count,
                request.dn,
                CompareFalseResponse.__name__,
            )
            response = CompareFalseResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].HOTP_COUNTER_EXCEEDED,
            )

        elif is_expired(
                oath_token_secret_time,
                oath_secret_max_age,
                now=self.now_dt,
                disable_secs=0,
            ):
            # fail because token's shared secret too old (is expired)
            self._log(
                logging.INFO,
                (
                    'Token %r of %r is expired '
                    '(oath_token_secret_time=%r, oath_secret_max_age=%r) => %s'
                ),
                oath_token_dn,
                request.dn,
                oath_token_secret_time,
                oath_secret_max_age,
                CompareFalseResponse.__name__,
            )
            response = CompareFalseResponse(
                request.msgid,
                self.infomsg[self.server.cfg.response_info].OTP_TOKEN_EXPIRED,
            )

        elif not otp_compare:
            # OTP value wrong
            self._log(
                logging.INFO,
                'HOTP verification failed for %r => %s',
                request.dn,
                CompareFalseResponse.__name__,
            )
            response = CompareFalseResponse(request.msgid)

        else:
            # Finally! Success!
            self._log(
                logging.INFO,
                'Validation ok for %r => response = success',
                request.dn,
            )
            response = CompareTrueResponse(request.msgid)

        return response
        # end of HOTPValidationHandler.do_compare()
