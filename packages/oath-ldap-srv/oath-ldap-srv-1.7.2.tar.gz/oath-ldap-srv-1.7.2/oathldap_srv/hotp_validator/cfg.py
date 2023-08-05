# -*- coding: utf-8 -*-
"""
oathldap_srv.hotp_validator.cfg
"""

import re

# from ldap0 package
from ldap0.ldapurl import LDAPUrl

from .. import cfg


DEBUG_VARS = [
    'oath_hotp_current_counter',
    'oath_hotp_lookahead',
    'oath_hotp_next_counter',
    'oath_max_usage_count',
    'oath_otp_length',
    'oath_params_dn',
    'oath_params_entry',
    'oath_secret_max_age',
    'oath_token_dn',
    'oath_token_identifier',
    'oath_token_identifier_length',
    'oath_token_identifier_req',
    'oath_token_secret_time',
    'otp_compare',
    'otp_value',
    'user_password_compare',
    'user_password_length',
]
if __debug__:
    # Only some sensitive variables if DEBUG=yes and in Python debug mode
    DEBUG_VARS.extend([
        'otp_token_entry',
        'user_entry',
        #'user_password_clear',
        'user_password_hash',
    ])


class HOTPValidatorConfig(cfg.Config):
    """
    Configuration parameters
    """
    default_section = 'hotp_validator'
    type_map = {
        'allowed_gids': cfg.val_list,
        'allowed_uids': cfg.val_list,
        'avg_count': int,
        'cache_ttl': float,
        'ldap0_trace_level': int,
        'ldap_cache_ttl': float,
        'ldapi_uri': LDAPUrl,
        'ldap_max_retries': int,
        'ldap_retry_delay': float,
        'ldap_timeout': float,
        'log_level': str.upper,
        'noproxy_peer_addrs': cfg.val_list,
        'providers': cfg.ldap_url_list,
        'proxy_peer_addrs': cfg.val_list,
        'proxy_peer_nets': cfg.ip_network_list,
        'socket_timeout': float,
        'threads': int,
        'token_cmp_regex': re.compile,
    }
    required_params = (
        'ldapi_uri',
        'socket_path',
    )

    # Configuration parameters
    #-------------------------------------------

    # size of thread pool
    threads = 2

    # time in seconds for which to cache bind requests
    # (set to negative number to disable caching)
    cache_ttl = -1.0

    # LDAPI URI for connecting to local slapd
    ldapi_uri = 'ldapi://'

    # CA certificate file to use for connecting to OATH-LDAP providers
    cacert_file = '/etc/ssl/ca-bundle.pem'

    # UIDs and peer GIDS of peers which are granted access
    # (list of int/strings)
    allowed_uids = [0, 'ldap']
    allowed_gids = [0]

    # String with octal representation of socket permissions
    socket_perms = '0666'

    # Trace level for ldap0 logs
    ldap0_trace_level = 0

    # Number of times connecting to local LDAPI is retried before sending a
    # failed response for a query
    ldap_max_retries = 10
    # Time to wait before retrying to connect within one query
    ldap_retry_delay = 0.1

    # SASL authz-ID to be sent along with SASL/EXTERNAL bind
    #ldapi_sasl_authzid = 'dn:uid=hotp_validator,dc=example,dc=com'
    ldapi_sasl_authzid = None

    # Time in seconds for which normal LDAP searches will be valid in cache
    ldap_cache_ttl = 180.0

    # Timeout in seconds when connecting to local and remote LDAP servers
    # used for ldap0.OPT_NETWORK_TIMEOUT and ldap0.OPT_TIMEOUT
    ldap_timeout = 3.0

    # Timeout in seconds for the server (Unix domain) socket
    socket_timeout = 2 * ldap_timeout

    # Base number for floating average value of response delay
    avg_count = 100

    log_vars = DEBUG_VARS

    # LDAP filter string for reading HOTP user entry
    user_filter = '(&(objectClass=oathHOTPUser)(oathHOTPToken=*))'

    # LDAP filter string for reading fully initialized HOTP token entry
    oath_token_filter = '(&(objectClass=oathHOTPToken)(oathHOTPCounter>=0)(oathSecret=*))'

    # Timestamp attributes which, if present, limit the
    # validity period of user entries
    user_notbefore_attr = 'aeNotBefore'
    #user_notbefore_attr = None
    user_notafter_attr = 'aeNotAfter'
    #user_notafter_attr = None

    # Time in seconds for which pwdPolicy and oathHOTPParams entries will be
    # valid in cache
    oath_params_cache_ttl = 600

    # Globbing pattern for searching JSON web key files (private keys)
    # used for decrypting the shared secrets
    # Setting this to None disables it and 'oathSecret'
    # is always assumed to contain the raw shared secret bytes
    primary_key_files = None

    # Set to True to return more information about what went wrong
    # in the response to the LDAP client
    response_info = __debug__

    # regex pattern defining whether request DN directly addresses a token entry
    token_cmp_regex = None


    def __init__(self, cfg_filename):
        cfg.Config.__init__(self, cfg_filename)
        self.cache_ttl = {
            'BIND': self.cache_ttl,
        }
