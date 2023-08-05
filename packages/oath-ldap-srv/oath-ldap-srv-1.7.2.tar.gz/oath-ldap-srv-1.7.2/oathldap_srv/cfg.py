# -*- coding: utf-8 -*-
"""
oathldap_srv.cfg - configuration vars
"""

import sys
import os
import ipaddress
from configparser import ConfigParser

from ldap0.ldapurl import LDAPUrl


def val_list(cfg_val):
    """
    Returns list of int or str values splitted from space- or
    comma-separated string with all white-spaces stripped
    """
    val_set = set()
    res = []
    for val in (cfg_val or '').strip().replace(',', '\n').replace(' ', '\n').split('\n'):
        val = val.strip()
        if val and val not in val_set:
            try:
                val = int(val)
            except ValueError:
                pass
            res.append(val)
            val_set.add(val)
    return res


def ldap_url_list(cfg_val):
    """
    Returns list of LDAPUrl instances from space- or comma-separated string
    """
    return [
        LDAPUrl(val)
        for val in val_list(cfg_val)
    ]


def ip_network_list(cfg_val):
    """
    Returns list of IPNetwork instances from space- or comma-separated string
    """
    return [
        ipaddress.ip_network(val)
        for val in val_list(cfg_val)
    ]


class Config:
    """
    method-less class containing all config params
    """
    default_section = None
    type_map = {
        'log_level': str.upper,
    }
    # names of required config parameters for which typically
    # no sensible defaults can be set as class attribute
    required_params = (())

    # Configuration parameters
    #-------------------------------------------

    # Pathname of Unix domain socket where slapd-sock sends requests to
    socket_path = None

    # Level of log details, see Python's standard logging module
    log_level = 'INFO'

    # logging configuration file
    log_config = None

    # logging qualifier name
    log_name = '{0}.{1}'.format(
        __name__.split('.')[0],
        os.path.basename(os.path.abspath(sys.argv[0])[:-3])
    )

    # Names of variables to send to debug output
    log_vars = []


    def __init__(self, cfg_filename):
        """
        read and parse config file into dict
        """
        if not os.path.exists(cfg_filename):
            raise SystemExit('Configuration file %r is missing!' % (cfg_filename,))
        cfg_parser = ConfigParser(
            interpolation=None,
            default_section=self.default_section,
        )
        cfg_parser.read([cfg_filename])
        for key in sorted(cfg_parser.defaults()):
            if not hasattr(self, key):
                raise SystemExit('Unknown config key-word %r' % (key,))
            type_func = self.type_map.get(key, str)
            raw_val = cfg_parser.get(self.default_section, key)
            try:
                val = type_func(raw_val)
            except ValueError:
                raise SystemExit('Invalid value for %r. Expected %s string, but got %r' % (
                    key, type_func.__name__, raw_val
                ))
            setattr(self, key, val)
        for key in self.required_params:
            if not hasattr(self, key) or getattr(self, key) is None:
                raise SystemExit('Mandatory config parameter %r missing' % (key,))
