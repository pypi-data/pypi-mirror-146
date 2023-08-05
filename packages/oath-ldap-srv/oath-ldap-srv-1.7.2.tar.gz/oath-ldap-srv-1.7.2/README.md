OATH-LDAP services
==================

[OATH-LDAP](https://oath-ldap.stroeder.com/) directly integrates
OTP-based two-factor authentication into
[OpenLDAP](https://www.openldap.org) *slapd*.

This package implements the slapd-sock BIND listener services:

  * HOTP validator
  * Bind Proxy

Requirements
------------

  * Python 3.6+

See also:

  * [slapd-sock(5)](https://www.openldap.org/software/man.cgi?query=slapd-sock)
