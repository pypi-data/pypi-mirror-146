# -*- coding: utf-8 -*-
"""
oathldap_srv.hotp_validator.server
"""

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

import json
import glob

from slapdsock.service import SlapdSockServer

# from jwcrypto
try:
    from jwcrypto.jwk import JWK
except ImportError:
    JWK = None

from .handler import HOTPValidationHandler

#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------

class HOTPValidationServer(SlapdSockServer):

    """
    This is used to pass in more parameters to the server instance.

    By purpose this is a single-threaded listener serializing all requests!
    """

    def __init__(self, cfg, logger):
        self.cfg = cfg
        SlapdSockServer.__init__(
            self,
            self.cfg.socket_path,
            HOTPValidationHandler,
            logger,
            self.cfg.avg_count,
            self.cfg.socket_timeout,
            self.cfg.socket_perms,
            self.cfg.allowed_uids,
            self.cfg.allowed_gids,
            bind_and_activate=True,
            monitor_dn=None,
            log_vars=cfg.log_vars,
            thread_pool_size=cfg.threads,
        )
        self.ldap_timeout = self.cfg.ldap_timeout
        self.ldapi_uri = self.cfg.ldapi_uri.connect_uri()
        self.ldap_trace_level = self.cfg.ldap0_trace_level
        self.ldap_authz_id = self.cfg.ldapi_sasl_authzid
        self.ldap_retry_max = self.cfg.ldap_max_retries
        self.ldap_retry_delay = self.cfg.ldap_retry_delay
        self.ldap_cache_ttl = self.cfg.ldap_cache_ttl
        self.max_lookahead_seen = 0
        if JWK:
            self._load_keys(self.cfg.primary_key_files, reset=True)
        # end of HOTPValidationServer.__init__()

    def _load_keys(self, key_files, reset=False):
        """
        Load JWE keys defined by globbing pattern in :key_files:
        """
        if reset:
            self.primary_keys = {}
        if not key_files:
            return
        self.logger.debug('Read JWK files with glob pattern %r', key_files)
        for private_key_filename in glob.glob(key_files):
            try:
                with open(private_key_filename, 'rb') as privkey_file:
                    privkey_json = privkey_file.read()
                private_key = JWK(**json.loads(privkey_json))
            except (IOError, ValueError) as err:
                self.logger.error(
                    'Error reading/decoding JWK file %r: %s',
                    private_key_filename,
                    err,
                )
            else:
                self.primary_keys[private_key['kid']] = private_key
        self.logger.info(
            'Read %d JWK files, key IDs: %s',
            len(self.primary_keys),
            ' '.join(self.primary_keys.keys()),
        )
        # end of _load_keys()

    def monitor_entry(self):
        """
        Returns entry dictionary with monitoring data.
        """
        monitor_entry = SlapdSockServer.monitor_entry(self)
        monitor_entry.update({
            'sockHOTPMaxLookAheadSeen': [str(self.max_lookahead_seen)],
            'sockHOTPKeyCount': [str(len(self.primary_keys))],
            'sockHOTPKeyIDs': self.primary_keys.keys(),
        })
        return monitor_entry
