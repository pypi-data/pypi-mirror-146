# -*- coding: utf-8 -*-
"""
package/install module package oathldap
"""

import sys
import os
from setuptools import setup, find_packages

PYPI_NAME = 'oath-ldap-srv'

BASEDIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.join(BASEDIR, 'oathldap_srv'))
import __about__

setup(
    name=PYPI_NAME,
    license=__about__.__license__,
    version=__about__.__version__,
    description='OATH-LDAP services',
    author=__about__.__author__,
    author_email=__about__.__mail__,
    maintainer=__about__.__author__,
    maintainer_email=__about__.__mail__,
    url='https://oath-ldap.stroeder.com',
    download_url='https://pypi.org/project/{0}/#files'.format(PYPI_NAME),
    keywords=['LDAP', 'OpenLDAP', 'OATH', 'OATH-LDAP', 'HOTP', 'TOTP', 'Yubikey'],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    #test_suite='tests',
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[],
    install_requires=[
        'setuptools',
        'ldap0 >= 1.2.1',
        'slapdsock>=1.3.0',
    ],
    extras_require={
        'hotp_validator':[
            'jwcrypto',
            'pynacl>=1.2',
        ],
    },
    zip_safe=False,
)
