# -*- coding: utf-8 -*-
"""
oathldap_srv.bind_proxy:
slapd-sock listener demon which sends intercepted BIND requests
to a remote LDAP server if needed
"""

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

# from Python's standard lib
import sys
import os
import os.path
import logging
import logging.config
import socket
import collections
import ipaddress
import time
import threading
import random

# from ldap0 package
import ldap0
from ldap0 import LDAPError
from ldap0.ldapurl import LDAPUrl
from ldap0.res import SearchResultEntry
from ldap0.ldapobject import ReconnectLDAPObject as LDAPObject
from ldap0.controls.sessiontrack import (
    SessionTrackingControl,
    SESSION_TRACKING_FORMAT_OID_USERNAME
)

# local modules
from slapdsock.ldaphelper import RESULT_CODE
from slapdsock.handler import SlapdSockHandler, SlapdSockHandlerError
from slapdsock.message import (
    CONTINUE_RESPONSE,
    InternalErrorResponse,
    RESULTResponse,
)

# run multi-threaded
from slapdsock.service import SlapdSockServer

from .__about__ import __version__
from . import cfg
from .logger import init_logger


# set of all bind-DNs enabled for OTP which shall be forwarded to provider
global OTP_ENABLED
OTP_ENABLED = None


#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------


class BindProxyConfig(cfg.Config):
    """
    Configuration parameters
    """
    default_section = 'bind_proxy'
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
        'ldap_unreachable_ttl': float,
        'log_level': str.upper,
        'noproxy_peer_addrs': cfg.val_list,
        'providers': cfg.ldap_url_list,
        'proxy_peer_addrs': cfg.val_list,
        'proxy_peer_nets': cfg.ip_network_list,
        'refresh_time': float,
        'socket_timeout': float,
        'proxy_user_min_count': int,
        'threads': int,
    }
    required_params = (
        'providers',
        'socket_path',
    )

    # Configuration parameters
    #-------------------------------------------

    # size of thread pool
    threads = 4

    # time in seconds for which to cache bind requests
    # (set to negative number to disable caching)
    cache_ttl = -1.0

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
    #ldapi_sasl_authzid = 'dn:uid=simple_bind_proxy,dc=example,dc=com'
    ldapi_sasl_authzid = None

    # Time in seconds for which normal LDAP searches will be valid in cache
    ldap_cache_ttl = 180.0

    # Time in seconds for which an unavailable OATH-LDAP provider will
    # not be tried for subsequent BIND requests
    ldap_unreachable_ttl = -1.0

    # Timeout in seconds when connecting to local and remote LDAP servers
    # used for ldap0.OPT_NETWORK_TIMEOUT and ldap0.OPT_TIMEOUT
    ldap_timeout = 3.0

    # Timeout in seconds for the server (Unix domain) socket
    socket_timeout = 2 * ldap_timeout

    # Base number for floating average value of response delay
    avg_count = 100

    # 1. peer addresses always excluded from proxying to OTP validator
    noproxy_peer_addrs = {
        '/run/slapd/ldapi',
        '127.0.0.1',
    }
    # 2. peer addresses proxied to OTP validator (after checking noproxy_peer_addrs)
    proxy_peer_addrs = {
    }
    # 3. peer address nets proxied to OTP validator (final check)
    proxy_peer_nets = (
        ipaddress.ip_network('0.0.0.0/0'),
    )

    # Space- or line separated list of LDAP URIs of OATH-LDAP providers
    providers = None

    # LDAP URI specifying the parameters for searching user entries for
    # which BIND requests have to be forwarded to OATH-LDAP providers
    # (set to None for disabling this check and forward all BIND requests)
    # Example:
    # proxy_user_search = 'ldap:///??sub?(oathToken=*)'
    proxy_user_search = None

    # minimum number of expected OTP-enabled user entries
    proxy_user_min_count = 1

    # Time (seconds) between refresh runs
    refresh_time = 60.0


    def __init__(self, cfg_filename):
        cfg.Config.__init__(self, cfg_filename)
        self.cache_ttl = {
            'BIND': self.cache_ttl,
        }


class RefreshThread(threading.Thread):
    """
    Update thread for retrieving SSH authorized keys and sudoers entries

    Thread is initialized by NSSPAMServer, started by main script
    """
    __slots__ = (
        'enabled',
        'schedule_interval',
        '_refresh_sleep',
        '_rand',
        'refresh_counter',
        'avg_refresh_time',
        'max_refresh_time',
        '_last_run',
        '_next_run',
        '_logger',
        '_ldapi_uri',
        '_ldapi_conn',
        'thread_pool_size',
    )
    avg_window = 30.0

    def __init__(self, scfg, logger):
        threading.Thread.__init__(
            self,
            group=None,
            target=None,
            name=None,
            args=(),
            kwargs={}
        )
        self._logger = logger
        self.enabled = True
        self.schedule_interval = 0.4
        self._cfg = scfg
        self._refresh_sleep = scfg.refresh_time
        self._rand_factor = scfg.refresh_time * 0.06
        self._proxy_user_search = LDAPUrl(scfg.proxy_user_search)
        self._rand = random.SystemRandom()
        self._ldapi_conn = None
        self.refresh_counter = 0
        self.avg_refresh_time = 0.0
        self.max_refresh_time = 0.0
        self._last_run = 0.0
        self._next_run = time.time()
        self.thread_pool_size = scfg.threads

    def _log(self, log_level, msg, *args, **kwargs):
        msg = ': '.join((self.__class__.__name__, msg))
        self._logger.log(log_level, msg, *args, **kwargs)

    def _refresh_task(self, ldap_conn):
        """
        refresh task
        """
        msg_id = ldap_conn.search(
            self._proxy_user_search.dn,
            self._proxy_user_search.scope,
            self._proxy_user_search.filterstr,
            attrlist=['1.1'],
        )
        proxy_users = set()
        for ldap_res in ldap_conn.results(msg_id):
            proxy_users.update([
                res.dn_s
                for res in ldap_res.rdata
                if isinstance(res, SearchResultEntry)
            ])
        self._log(
            (
                logging.INFO
                if len(proxy_users) >= self._cfg.proxy_user_min_count
                else logging.ERROR
            ),
            'Found %d OTP-enabled user entries on %r with filter: %r',
            len(proxy_users),
            ldap_conn.uri,
            self._proxy_user_search.filterstr,
        )
        global OTP_ENABLED
        OTP_ENABLED = proxy_users
        # end of _refresh_task()

    @property
    def ldapi_conn(self):
        """
        return a local LDAPI connection to OATH-LDAP server
        """
        if self._ldapi_conn is None:
            self._logger.debug('Connecting to %r...', self._proxy_user_search.connect_uri())
            try:
                self._ldapi_conn = LDAPObject(
                    self._proxy_user_search.connect_uri(),
                    trace_level=self._cfg.ldap0_trace_level,
                    retry_max=self._cfg.ldap_max_retries,
                    retry_delay=self._cfg.ldap_retry_delay,
                )
                self._ldapi_conn.sasl_non_interactive_bind_s('EXTERNAL')
            except ldap0.SERVER_DOWN as ldap_error:
                self._logger.error(
                    'Connecting to %r failed: %s',
                    self._proxy_user_search.connect_uri(),
                    ldap_error,
                )
                self._ldapi_conn = None
                raise ldap_error
            self._logger.debug(
                'Connected to %r bound as %r',
                self._ldapi_conn.uri,
                self._ldapi_conn.whoami_s(),
            )
        return self._ldapi_conn

    def run(self):
        """
        retrieve data forever
        """
        self._log(logging.DEBUG, 'Starting %s.run()', self.__class__.__name__)
        while self.enabled:
            start_time = time.time()
            if start_time > self._next_run:
                self._log(logging.DEBUG, 'Invoking %s._refresh_task()', self.__class__.__name__)
                try:
                    self._refresh_task(self.ldapi_conn)
                    self.refresh_counter += 1
                    refresh_time = time.time() - start_time
                    if self.max_refresh_time < refresh_time:
                        self.max_refresh_time = refresh_time
                    avg_window = min(self.avg_window, self.refresh_counter)
                    self.avg_refresh_time = (
                        ((avg_window - 1) * self.avg_refresh_time + refresh_time) / avg_window
                    )
                    self._log(
                        logging.INFO,
                        '%d. refresh run with %s (%0.3f secs, avg: %0.3f secs)',
                        self.refresh_counter,
                        self.ldapi_conn.uri,
                        refresh_time,
                        self.avg_refresh_time,
                    )
                except ldap0.SERVER_DOWN as ldap_error:
                    self._log(
                        logging.WARN,
                        'Invalid connection: %s',
                        ldap_error,
                    )
                    self._ldapi_conn = None
                except Exception:
                    self._log(
                        logging.ERROR,
                        'Aborted refresh with unhandled exception',
                        exc_info=True,
                    )
                self._last_run = start_time
                self._next_run = (
                    time.time() +
                    self._refresh_sleep +
                    self._rand_factor * self._rand.random()
                )
            time.sleep(self.schedule_interval)
        self._log(logging.DEBUG, 'Exiting %s.run()', self.__class__.__name__)
        # end of RefreshThread.run()


class BindProxyHandler(SlapdSockHandler):

    """
    Handler class which proxies some simple bind requests to remote server
    """

    def _check_peername(self, peer):
        peer_type, peer_addr = peer.lower().rsplit(':', 1)[0].split('=')
        if peer_addr in self.server.cfg.noproxy_peer_addrs:
            self._log(logging.DEBUG, 'Peer %r explicitly excluded => no OTP check', peer_addr)
            return False
        if peer_addr in self.server.cfg.proxy_peer_addrs:
            self._log(logging.DEBUG, 'Peer %r explicitly included => proxy OTP check', peer_addr)
            return True
        if not peer_type == 'ip':
            self._log(logging.DEBUG, 'Peer %r not an IP address => no OTP check', peer_addr)
            return False
        peer_ip_address = ipaddress.ip_address(peer_addr.replace('[', '').replace(']', ''))
        for peer_net in self.server.cfg.proxy_peer_nets:
            if peer_ip_address in peer_net:
                self._log(
                    logging.DEBUG,
                    'Peer %r in included net %r => proxy OTP check',
                    peer_ip_address,
                    peer_net,
                )
                return True
        self._log(logging.DEBUG, 'Peer %r not included => no OTP check', peer_addr)
        return False # end of _check_peername()

    def _shuffle_providers(self, request):
        """
        Generate list of upstream LDAP URIs shifted based on bind-DN hash
        """
        current_time = time.time()
        ldap_uris = collections.deque([
            uri
            for uri, lock_time in self.server.providers.items()
            if lock_time <= current_time
        ])
        if len(ldap_uris) > 1:
            ldap_uris.rotate(hash(request.dn) % len(ldap_uris))
        return ldap_uris

    def _check_user(self, request):
        """
        Additional check whether bind request has to be sent to remote LDAP
        server by searching the bind-DN's entry with a filter
        """
        if self.server.cfg.proxy_user_search is None:
            return
        if OTP_ENABLED is None:
            self._log(
                logging.DEBUG,
                'OTP_ENABLED not yet initialized',
            )
            raise SlapdSockHandlerError(
                'OTP_ENABLED not yet initialized',
                log_level=logging.INFO,
                response=InternalErrorResponse(request.msgid),
                log_vars=self.server.cfg.log_vars,
            )
        if request.dn in OTP_ENABLED:
            self._log(
                logging.DEBUG,
                '%r is in OTP_ENABLED => send to provider',
                request.dn,
            )
            return
        raise SlapdSockHandlerError(
            '{!r} not in OTP_ENABLED'.format(request.dn),
            log_level=logging.INFO,
            response=CONTINUE_RESPONSE,
            log_vars=self.server.cfg.log_vars,
        )
        # end of _check_user()

    def do_bind(self, request):
        """
        This method first checks whether the BIND request must be sent
        to the upstream replica
        """

        if not self._check_peername(request.peername):
            self._log(
                logging.DEBUG,
                'Peer %r not in %r and %r => let slapd continue',
                request.peername,
                self.server.cfg.proxy_peer_addrs,
                self.server.cfg.proxy_peer_nets,
            )
            return CONTINUE_RESPONSE

        self._check_user(request)

        providers = self._shuffle_providers(request)
        self._log(logging.DEBUG, 'providers = %r', providers)

        try:
            try:
                while providers:
                    remote_ldap_uri = providers.popleft()
                    self._log(logging.DEBUG, 'Sending request to %r', remote_ldap_uri)
                    try:
                        remote_ldap_conn = LDAPObject(
                            remote_ldap_uri,
                            trace_level=0,
                        )
                        remote_ldap_conn.set_tls_options(
                            cacert_filename=self.server.cfg.cacert_file,
                        )
                        remote_ldap_conn.simple_bind_s(
                            request.dn,
                            request.cred,
                            req_ctrls=[
                                SessionTrackingControl(
                                    request.peername,
                                    socket.getfqdn(),
                                    SESSION_TRACKING_FORMAT_OID_USERNAME,
                                    request.dn,
                                ),
                            ]
                        )
                    except ldap0.SERVER_DOWN as ldap_error:
                        self.server.providers[remote_ldap_uri] = (
                            time.time() + self.server.cfg.ldap_unreachable_ttl
                        )
                        self._log(
                            logging.WARN,
                            'Connecting to %r failed: %s => try next',
                            remote_ldap_uri,
                            ldap_error,
                        )
                    else:
                        break
                else:
                    raise SlapdSockHandlerError(
                        'Could not connect to any provider!',
                        log_level=logging.ERROR,
                        response=RESULTResponse(
                            request.msgid,
                            RESULT_CODE['unavailable'],
                            info='OATH providers unavailable',
                        ),
                        log_vars=self.server._log_vars,
                    )
            except LDAPError as ldap_error:
                try:
                    result_code = RESULT_CODE[type(ldap_error)]
                except KeyError:
                    result_code = RESULT_CODE['other']
                try:
                    info = ldap_error.args[0]['info'].decode('utf-8')
                except (AttributeError, KeyError, TypeError):
                    info = None
                self._log(
                    logging.ERROR,
                    'LDAPError from %s: %s => return %s %r',
                    remote_ldap_uri,
                    ldap_error,
                    ldap_error,
                    result_code,
                )
            else:
                # Prepare the success result returned
                result_code = 'success'
                info = None
                self._log(
                    logging.INFO,
                    'Validation ok for %r (from %r) using provider %r => RESULT: %s',
                    request.dn,
                    request.peername,
                    remote_ldap_conn.uri,
                    result_code,
                )
        finally:
            try:
                remote_ldap_conn.unbind_s()
            except Exception:
                pass

        self._log(
            logging.DEBUG,
            'msgid=%s result_code=%s info=%s',
            request.msgid,
            result_code,
            info,
        )
        return RESULTResponse(
            request.msgid,
            result_code,
            info=info
        )
        # end of do_bind()


class BindProxyServer(SlapdSockServer):

    """
    This is used to pass in more parameters to the server instance
    """
    thread_pool_size = 4

    def __init__(self, scfg, logger):
        self.cfg = scfg
        SlapdSockServer.__init__(
            self,
            self.cfg.socket_path,
            BindProxyHandler,
            logger,
            self.cfg.avg_count,
            self.cfg.socket_timeout,
            self.cfg.socket_perms,
            self.cfg.allowed_uids,
            self.cfg.allowed_gids,
            bind_and_activate=True,
            monitor_dn=None,
            log_vars=self.cfg.log_vars,
            thread_pool_size=self.cfg.threads,
        )
        self.ldap_trace_level = self.cfg.ldap0_trace_level
        self.providers = {}.fromkeys(
            [ldap_uri.connect_uri() for ldap_uri in self.cfg.providers],
            0.0,
        )


#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------

def run():
    """
    The main script
    """
    # read config from file
    scfg = BindProxyConfig(sys.argv[1])

    # initialize a custom logger from config
    my_logger = init_logger(scfg)

    my_logger.info(
        'Starting %s %s (log level %d)',
        os.path.basename(os.path.abspath(sys.argv[0])),
        __version__,
        my_logger.level
    )

    # log all configuration attributes
    for name in sorted(dir(scfg)):
        if not name.startswith('__'):
            my_logger.debug('%s.%s = %r', scfg.__class__.__name__, name, getattr(scfg, name))

    # log all configuration attributes
    for name in sorted(dir(scfg)):
        if not name.startswith('__'):
            my_logger.debug('%s.%s = %r', scfg.__class__.__name__, name, getattr(scfg, name))

    if __debug__:
        my_logger.error(
            (
                '!!! Running in debug mode (log level %d)! '
                'Secret data will be logged! '
                'Don\'t do that!!!'
            ),
            my_logger.level
        )

    refresh_thread = RefreshThread(scfg, my_logger)

    try:
        refresh_thread.start()
        slapd_sock_listener = BindProxyServer(scfg, my_logger)
        try:
            slapd_sock_listener.serve_forever()
        except KeyboardInterrupt:
            my_logger.warning('Received interrupt signal => shutdown')
    finally:
        my_logger.debug('Stopping refresh thread')
        refresh_thread.enabled = False
        my_logger.debug('Removing socket path %r', scfg.socket_path)
        try:
            os.remove(scfg.socket_path)
        except OSError:
            pass

    # end of run()


if __name__ == '__main__':
    run()
