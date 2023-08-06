# -*- coding: ascii -*-
"""
Automatic tests for simple functions in module aedir

See https://ae-dir.com/python.html for details.
"""

# from Python's standard lib
import os
import unittest

# env vars must be set before importing ldap0
os.environ['LDAPCONF'] = os.environ['LDAPRC'] = os.path.join(os.path.dirname(__file__), 'ldap_aedir_test.conf')

# from ldap0
import ldap0
from ldap0.ldapurl import LDAPUrl

# import module to be tested herein
import aedir

# set python-ldap's trace level
ldap0._trace_level = 0


class TestAedirFuncs(unittest.TestCase):
    """
    test all simple functions
    """

    def test_extract_zone(self):
        """
        test function extract_zone()
        """
        self.assertEqual(
            aedir.extract_zone(
                'cn=foo,cn=bar,ou=ae-dir'
            ),
            'bar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'cn=foobar,ou=ae-dir'
            ),
            'foobar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'uid=xkcd,cn=foobar,ou=ae-dir'
            ),
            'foobar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'cn=foo,cn=bar,ou=ae-dir', aeroot_dn='ou=ae-dir'
            ),
            'bar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'cn=foobar,ou=ae-dir', aeroot_dn='ou=ae-dir'
            ),
            'foobar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'uid=xkcd,cn=foobar,ou=ae-dir', aeroot_dn='ou=ae-dir'
            ),
            'foobar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'cn=foo,cn=bar,dc=example,dc=com', aeroot_dn='dc=example,dc=com'
            ),
            'bar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'cn=foobar,dc=example,dc=com', aeroot_dn='dc=example,dc=com'
            ),
            'foobar'
        )
        self.assertEqual(
            aedir.extract_zone(
                'uid=xkcd,cn=foobar,dc=example,dc=com', aeroot_dn='dc=example,dc=com'
            ),
            'foobar'
        )
        with self.assertRaises(ValueError):
            aedir.extract_zone(
                'cn=foo,cn=bar,ou=ae-dir-x',
                aeroot_dn='ou=ae-dir'
            )

    def test_aedir_aeuser_dn(self):
        """
        test function aedir_aeuser_dn()
        """
        self.assertEqual(
            aedir.aedir_aeuser_dn('foo'),
            'uid=foo,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aeuser_dn('foo', 'bar'),
            'uid=foo,cn=bar,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aeuser_dn('foo@bar'),
            'uid=foo,cn=bar,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aeuser_dn('foo', zone='bar'),
            'uid=foo,cn=bar,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aeuser_dn(
                'foo', zone='bar', aeroot_dn='dc=example,dc=com'
            ),
            'uid=foo,cn=bar,dc=example,dc=com'
        )

    def test_aedir_aegroup_dn(self):
        """
        test function aedir_aegroup_dn()
        """
        self.assertEqual(
            aedir.aedir_aegroup_dn('foo-bar-1'),
            'cn=foo-bar-1,cn=foo,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aegroup_dn('foo-bar-1', aeroot_dn='dc=example,dc=com'),
            'cn=foo-bar-1,cn=foo,dc=example,dc=com'
        )
        with self.assertRaises(ValueError):
            aedir.aedir_aegroup_dn('foo1')

    def test_aedir_aehost_dn(self):
        """
        test function aedir_aehost_dn()
        """
        self.assertEqual(
            aedir.aedir_aehost_dn('foo.example.com'),
            'host=foo.example.com,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aehost_dn('foo.example.com', 'bar', 'bar'),
            'host=foo.example.com,cn=bar,cn=bar,ou=ae-dir'
        )
        self.assertEqual(
            aedir.aedir_aehost_dn(
                'foo.example.com',
                srvgrp='bar',
                aeroot_dn='dc=example,dc=com'
            ),
            'host=foo.example.com,dc=example,dc=com'
        )
        self.assertEqual(
            aedir.aedir_aehost_dn(
                'foo.example.com',
                srvgrp='bar1',
                zone='bar2',
                aeroot_dn='dc=example,dc=com'
            ),
            'host=foo.example.com,cn=bar1,cn=bar2,dc=example,dc=com'
        )
        self.assertEqual(
            aedir.aedir_aehost_dn(
                'foo.example.com',
                zone='bar',
                aeroot_dn='dc=example,dc=com'
            ),
            'host=foo.example.com,dc=example,dc=com'
        )

    def test_ldap_conf_url(self):
        ldap_url = aedir.ldap_conf_url()
        self.assertIsInstance(ldap_url, aedir.AEDirUrl)
        self.assertIsInstance(ldap_url, LDAPUrl)
        self.assertEqual(ldap_url.urlscheme, 'ldaps')
        self.assertEqual(ldap_url.hostport, 'ae-dir.example.com:636')
        self.assertEqual(ldap_url.dn, 'dc=ae-dir,dc=example,dc=com')
        self.assertEqual(
            str(ldap_url),
            'ldaps://ae-dir.example.com:636/dc%3Dae-dir%2Cdc%3Dexample%2Cdc%3Dcom???'
        )
        ldap_url = aedir.ldap_conf_url(LDAPUrl)
        self.assertIsInstance(ldap_url, LDAPUrl)
        self.assertFalse(isinstance(ldap_url, aedir.AEDirUrl))


if __name__ == '__main__':
    unittest.main()
