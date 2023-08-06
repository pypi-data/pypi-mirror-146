# -*- coding: ascii -*-
"""
slapdsock.test - base classes for unit tests

slapdsock - OpenLDAP back-sock listeners with Python
see https://code.stroeder.com/pymod/python-slapdsock

(c) 2015-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

# from ldap0 package
import ldap0.test

from .service import SlapdSockServer
from .handler import NoopHandler

__all__ = [
    'SlapdObject',
    'SlapdSockTest',
]


# a template string for generating simple slapd.conf file
SLAPD_CONF_TEMPLATE = r"""
serverID %(serverid)s
moduleload back_%(database)s
include "%(schema_include)s"
loglevel %(loglevel)s
allow bind_v2

authz-regexp
  "gidnumber=%(root_gid)s\\+uidnumber=%(root_uid)s,cn=peercred,cn=external,cn=auth"
  "%(rootdn)s"

database %(database)s
directory "%(directory)s"
suffix "%(suffix)s"
rootdn "%(rootdn)s"
rootpw "%(rootpw)s"
"""


class SlapdObject(ldap0.test.SlapdObject):
    """
    run test slapd process
    """
    database = 'sock'
    slapd_conf_template = SLAPD_CONF_TEMPLATE
    suffix = 'dc=slapdsock,dc=stroeder,dc=com'


class SlapdSockTest(ldap0.test.SlapdTestCase):
    """
    test class which initializes an slapd with back-sock
    """

    server_class = SlapdObject
    slapdsock_server_class = SlapdSockServer
    slapdsock_handler_class = NoopHandler
    init_ldif_file = None

    @classmethod
    def setUpClass(cls):
        cls.server = cls.server_class()
        cls.server.start()
        cls.server = cls.server

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
