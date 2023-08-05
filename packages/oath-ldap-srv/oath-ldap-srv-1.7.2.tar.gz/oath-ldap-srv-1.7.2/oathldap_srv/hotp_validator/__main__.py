# -*- coding: utf-8 -*-
"""
oathldap_srv.hotp_validator.__main__ - entry point
"""

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

# from Python's standard lib
import os
import sys

from ..__about__ import __version__
from ..logger import init_logger

from .cfg import HOTPValidatorConfig
from .server import HOTPValidationServer


def run():
    """
    The main script
    """
    # read config from file
    scfg = HOTPValidatorConfig(sys.argv[1])

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

    if __debug__:
        my_logger.error(
            (
                '!!! Running in debug mode (log level %d)! '
                'Secret data will be logged! '
                'Don\'t do that!!!'
            ),
            my_logger.level
        )

    try:
        slapd_sock_listener = HOTPValidationServer(scfg, my_logger)
        try:
            slapd_sock_listener.serve_forever()
        except KeyboardInterrupt:
            my_logger.warning('Received interrupt signal => shutdown')
    finally:
        my_logger.debug('Removing socket path %r', scfg.socket_path)
        try:
            os.remove(scfg.socket_path)
        except OSError:
            pass

    # end of run()


if __name__ == '__main__':
    run()
