# -*- coding: ascii -*-
"""
Automatic unit tests for class aedir.AEDirObject
"""

import os
import unittest

import ldap0
from ldap0.err import NoUniqueEntry
from ldap0.base import decode_list, decode_entry_dict
from ldap0.dn import DNObj
from ldap0.controls.deref import DereferenceControl

from aedir.test import AETest
from aedir import AEDirUrl, AEDirObject
from aedir.models import (
    AEGroup,
    AEHost,
    AESrvGroup,
)



class Test01AEDirObject(AETest):
    """
    test class aedir.AEDirObject
    """

    def test001_search_base(self):
        with self._get_conn() as aedir_conn:
            self.assertEqual(aedir_conn.search_base, self.ae_suffix)
            self.assertEqual(str(aedir_conn.search_base_dnobj), self.ae_suffix)
        # now with forced anonymous bind
        with self._get_conn(who='', cred=b'') as anon_aedir_conn:
            self.assertEqual(anon_aedir_conn.whoami_s(), '')
            self.assertEqual(aedir_conn.search_base, self.ae_suffix)
            self.assertEqual(str(aedir_conn.search_base_dnobj), self.ae_suffix)

    def test002a_root_whoami_s(self):
        with self._get_conn() as aedir_conn:
            self.assertEqual(
                aedir_conn.whoami_s(),
                'dn:cn=root,'+self.ae_suffix
            )
        server = list(self.servers.values())[0]
        for uri in (
#            None,
            server.ldapi_uri,
            AEDirUrl(server.ldapi_uri),
        ):
            with AEDirObject(uri, who=None, cred=None) as aedir_conn:
                self.assertEqual(
                    aedir_conn.whoami_s(),
                    'dn:cn=root,'+self.ae_suffix
                )

    def test002b_authzid_whoami_s(self):
        sasl_authz_id = 'dn:uid=msin,cn=ae,' + self.ae_suffix
        with self._get_conn(sasl_authz_id=sasl_authz_id) as aedir_conn:
            self.assertEqual(aedir_conn.whoami_s(), sasl_authz_id)
        with self._get_conn(sasl_authz_id='u:msin') as aedir_conn:
            self.assertEqual(aedir_conn.whoami_s(), sasl_authz_id)

    def test003_find_uid(self):
        with self._get_conn() as aedir_conn:
            msin = aedir_conn.find_uid('msin')
            self.assertEqual(
                (msin.dn_s, msin.entry_s),
                (
                    'uid=msin,cn=ae,'+self.ae_suffix,
                    {
                        'aeTicketId': ['INIT-42'],
                        'displayName': ['Michael Str\xF6der (msin/30000)'],
                        'description': ['initial \xC6-DIR admin'],
                        'objectClass': [
                            'account', 'person', 'organizationalPerson',
                            'inetOrgPerson', 'aeObject', 'aeUser',
                            'posixAccount', 'aeSSHAccount'
                        ],
                        'loginShell': ['/bin/bash'],
                        'aeStatus': ['0'],
                        'gidNumber': ['30000'],
                        'givenName': ['Michael'],
                        'sn': ['Str\xF6der'],
                        'homeDirectory': ['/home/msin'],
                        'uid': ['msin'],
                        'mail': ['michael@stroeder.com'],
                        'uidNumber': ['30000'],
                        'aeTag': ['ae-tag-init', 'pub-tag-no-welcome-yet'],
                        'aePerson': ['uniqueIdentifier=INIT-PERSON-ID-42,cn=people,ou=ae-dir'],
                        'cn': ['Michael Str\xF6der']
                    },
                ),
            )
            msin = aedir_conn.find_uid('msin', attrlist=['uid', 'cn', 'memberOf'])
            self.assertEqual(
                (msin.dn_s, msin.entry_s),
                (
                    'uid=msin,cn=ae,'+self.ae_suffix,
                    {
                        'uid': ['msin'],
                        'cn': ['Michael Str\xF6der'],
                        'memberOf': ['cn=ae-admins,cn=ae,ou=ae-dir'],
                    },
                ),
            )


    def test004_get_user_groups(self):
        with self._get_conn() as aedir_conn:
            self.assertEqual(
                aedir_conn.get_user_groups('msin'),
                set(['cn=ae-admins,cn=ae,ou=ae-dir']),
            )
            self.assertEqual(
                aedir_conn.get_user_groups('msin', memberof_attr=None),
                set(['cn=ae-admins,cn=ae,ou=ae-dir']),
            )
            self.assertEqual(
                aedir_conn.get_user_groups('msin', memberof_attr='memberOf'),
                set(['cn=ae-admins,cn=ae,ou=ae-dir']),
            )

    def test005a_full_simple_bind(self):
        with self._get_conn(
            who='uid=bccb,cn=test,ou=ae-dir',
            cred=b'Geheimer123456',
        ) as aedir_conn:
            self.assertEqual(aedir_conn.whoami_s(), 'dn:uid=bccb,cn=test,'+self.ae_suffix)
            self.assertEqual(aedir_conn.get_whoami_dn(), 'uid=bccb,cn=test,'+self.ae_suffix)

    def test005b_short_simple_bind(self):
        with self._get_conn(
            who='uid=bccb,ou=ae-dir',
            cred=b'Geheimer123456',
        ) as aedir_conn:
            self.assertEqual(aedir_conn.whoami_s(), 'dn:uid=bccb,cn=test,'+self.ae_suffix)
            self.assertEqual(aedir_conn.get_whoami_dn(), 'uid=bccb,cn=test,'+self.ae_suffix)

    def test005c_anon_bind(self):
        with self._get_conn(
            who='',
            cred=b'',
        ) as aedir_conn:
            self.assertEqual(aedir_conn.whoami_s(), '')
            self.assertEqual(aedir_conn.get_whoami_dn(), '')

    def test006_get_zoneadmins(self):
        with self._get_conn() as aedir_conn:
            zone_admins = aedir_conn.get_zoneadmins(
                'cn=test,ou=ae-dir',
                attrlist=['mail', 'cn'],
            )
            self.assertEqual(
                [
                    (res.dn_s, res.entry_s)
                    for res in sorted(zone_admins, key=lambda x: x.dn_s)
                ],
                [
                    (
                        'uid=bccb,cn=test,ou=ae-dir',
                        {
                            'mail': ['michael@stroeder.com'],
                            'cn': ['Michael Str\xF6der']
                        }
                    )
                ],
            )

    def test007_find_aehost(self):
        with self._get_conn() as aedir_conn:
            aehost = aedir_conn.find_aehost('foo.example.com', attrlist=['*'])
            self.assertEqual(
                aehost.dn_s,
                'host=foo.example.com,cn=test-services-1,cn=test,'+self.ae_suffix
            )
            ldap_entry = aehost.ldap_entry()
            ldap_entry['objectClass'].sort()
            self.assertEqual(
                ldap_entry,
                {
                    'aeNotBefore': [b'20170116213536Z'],
                    'aeSrvGroup': [b'cn=test-services-2,cn=test,ou=ae-dir'],
                    'aeStatus': [b'0'],
                    'cn': [b'foo'],
                    'host': [b'foo.example.com'],
                    'objectClass': [b'aeDevice', b'aeHost', b'aeObject', b'device', b'ldapPublicKey'],
                }
            )

    def test008_get_service_groups(self):
        with self._get_conn() as aedir_conn:
            aehost_dn = 'host=foo.example.com,cn=test-services-1,cn=test,'+self.ae_suffix
            ae_srv_groups = []
            for res in aedir_conn.get_service_groups(aehost_dn):
                ae_srv_groups.extend(res.rdata)
            self.assertEqual(
                sorted([(asg.dn_s, asg.entry_s) for asg in ae_srv_groups]),
                [
                    (str(DNObj.from_str(aehost_dn).parent()), {}),
                    ('cn=test-services-2,cn=test,ou=ae-dir', {}),
                ]
            )
            ae_srv_groups = []
            for res in aedir_conn.get_service_groups(aehost_dn, attrlist=['cn']):
                ae_srv_groups.extend(res.rdata)
            self.assertEqual(
                sorted([(asg.dn_s, asg.entry_s) for asg in ae_srv_groups]),
                [
                    (str(DNObj.from_str(aehost_dn).parent()), {'cn': ['test-services-1']}),
                    ('cn=test-services-2,cn=test,ou=ae-dir', {'cn': ['test-services-2']}),
                ]
            )

    def test010_get_service_groups(self):
        with self._get_conn() as aedir_conn:
            aehost_dn = 'host=foo.example.com,cn=test-services-1,cn=test,' + self.ae_suffix
            ae_srv_groups = []
            for res in aedir_conn.get_service_groups(aehost_dn):
                ae_srv_groups.extend(res.rdata)
            self.assertEqual(
                sorted([(asg.dn_s, asg.entry_s) for asg in ae_srv_groups]),
                [
                    ('cn=test-services-1,cn=test,ou=ae-dir', {}),
                    ('cn=test-services-2,cn=test,ou=ae-dir', {}),
                ]
            )
            ae_srv_groups = []
            for res in aedir_conn.get_service_groups(aehost_dn, attrlist=['cn']):
                ae_srv_groups.extend(res.rdata)
            self.assertEqual(
                sorted([(asg.dn_s, asg.entry_s) for asg in ae_srv_groups]),
                [
                    ('cn=test-services-1,cn=test,ou=ae-dir', {'cn': ['test-services-1']}),
                    ('cn=test-services-2,cn=test,ou=ae-dir', {'cn': ['test-services-2']}),
                ]
            )
            ae_srv_groups = []
            for res in aedir_conn.get_service_groups(aehost_dn, filterstr='(cn=*-2)'):
                ae_srv_groups.extend(res.rdata)
            self.assertEqual(
                sorted([(asg.dn_s, asg.entry_s) for asg in ae_srv_groups]),
                [
                    ('cn=test-services-2,cn=test,ou=ae-dir', {}),
                ]
            )

    def test010_get_service_groups_deref(self):
        """
        same like .test010_get_service_groups() but with deref control
        """
        with self._get_conn() as aedir_conn:
            aehost_dn = 'host=foo.example.com,cn=test-services-1,cn=test,' + self.ae_suffix
            ae_srv_groups = []
            # test with deref control
            ae_srv_groups = []
            for res in aedir_conn.get_service_groups(
                    aehost_dn,
                    attrlist=['cn'],
                    req_ctrls=[DereferenceControl(
                        True,
                        {
                            'aeVisibleGroups': ['gidNumber', 'memberUid'],
                            'aeVisibleSudoers': ['sudoCommand', 'sudoHost', 'sudoUser'],
                        }
                    )],
                ):
                ae_srv_groups.extend(res.rdata)
            self.assertEqual(
                sorted([(asg.dn_s, asg.entry_s) for asg in ae_srv_groups]),
                [
                    ('cn=test-services-1,cn=test,ou=ae-dir', {'cn': ['test-services-1']}),
                    ('cn=test-services-2,cn=test,ou=ae-dir', {'cn': ['test-services-2']}),
                ]
            )
            # check response control type
            for asg in ae_srv_groups:
                self.assertEqual(asg.ctrls[0].controlType, '1.3.6.1.4.1.4203.666.5.16')
            self.assertEqual(
                sorted([
                    (
                        asg.dn_s,
                        sorted([
                            dref.entry_s
                            for dref in asg.ctrls[0].derefRes['aeVisibleGroups']
                        ])
                    )
                    for asg in ae_srv_groups
                ]),
                [
                    ('cn=test-services-1,cn=test,ou=ae-dir', [{'gidNumber': ['30023'], 'memberUid': ['wxrl', 'xkcd']}]),
                    ('cn=test-services-2,cn=test,ou=ae-dir', [{'gidNumber': ['30024'], 'memberUid': ['bccb', 'luua']}]),
                ]
            )

    def test011_get_user_srvgroup_relations(self):
        with self._get_conn() as aedir_conn:
            aesrvgroup_dn = 'cn=test-services-1,cn=test,' + self.ae_suffix
            srv_rels = aedir_conn.get_user_srvgroup_relations('xkcd', aesrvgroup_dn)
            self.assertEqual(sorted(srv_rels), ['aeLoginGroups', 'aeVisibleGroups'])
            srv_rels = aedir_conn.get_user_srvgroup_relations('xkcd', aesrvgroup_dn, ['aeSetupGroups'])
            self.assertEqual(sorted(srv_rels), [])
            srv_rels = aedir_conn.get_user_srvgroup_relations('wxrl', aesrvgroup_dn)
            self.assertEqual(sorted(srv_rels), ['aeLoginGroups', 'aeSetupGroups', 'aeVisibleGroups'])
            srv_rels = aedir_conn.get_user_srvgroup_relations('wxrl', aesrvgroup_dn, ['aeLoginGroups'])
            self.assertEqual(sorted(srv_rels), ['aeLoginGroups'])

    def test012_get_user_service_relations(self):
        with self._get_conn() as aedir_conn:
            aehost_dn = 'host=foo.example.com,cn=test-services-1,cn=test,' + self.ae_suffix
            srv_rels = aedir_conn.get_user_service_relations('xkcd', aehost_dn)
            self.assertEqual(srv_rels, set(['aeLoginGroups', 'aeVisibleGroups']))
            srv_rels = aedir_conn.get_user_service_relations('xkcd', aehost_dn, ['aeLoginGroups'])
            self.assertEqual(srv_rels, set(['aeLoginGroups']))
            srv_rels = aedir_conn.get_user_service_relations('wxrl', aehost_dn)
            self.assertEqual(srv_rels, set(['aeLoginGroups', 'aeSetupGroups', 'aeVisibleGroups']))
            srv_rels = aedir_conn.get_user_service_relations('wxrl', aehost_dn, ['aeLoginGroups'])
            self.assertEqual(srv_rels, set(['aeLoginGroups']))
            # test relationship via auxiliary aeSrvGroup attribute
            srv_rels = aedir_conn.get_user_service_relations('bccb', aehost_dn)
            self.assertEqual(sorted(srv_rels), ['aeLoginGroups', 'aeVisibleGroups'])
            srv_rels = aedir_conn.get_user_service_relations('bccb', aehost_dn, ['aeLoginGroups'])
            self.assertEqual(sorted(srv_rels), ['aeLoginGroups'])

    def test013_get_users(self):
        with self._get_conn() as aedir_conn:
            aehost_dn = 'host=foo.example.com,cn=test-services-1,cn=test,' + self.ae_suffix
            self.assertEqual(
                tuple([
                    (
                        u.rtype,
                        [(d.dn_b, d.entry_b) for d in u.rdata],
                        u.msgid,
                        u.ctrls,
                    )
                    for u in aedir_conn.get_users(
                        aehost_dn,
                        attrlist=['uid', 'cn', 'uidNumber', 'memberOf'],
                    )
                ]),
                (
                    (
                        100,
                        [
                            (
                                b'uid=bccb,cn=test,ou=ae-dir',
                                {
                                    b'cn': [b'Michael Str\xc3\xb6der'],
                                    b'uid': [b'bccb'],
                                    b'uidNumber': [b'30022'],
                                    b'memberOf': [
                                        b'cn=test-users-2,cn=test,ou=ae-dir',
                                        b'cn=test-zone-admins,cn=test,ou=ae-dir',
                                    ],
                                }
                            ),
                         ],
                        5,
                        [],
                    ),
                    (
                        100,
                        [
                            (
                                b'uid=luua,cn=test,ou=ae-dir',
                                {
                                    b'cn': [b'Michael Str\xc3\xb6der'],
                                    b'uid': [b'luua'],
                                    b'uidNumber': [b'30025'],
                                    b'memberOf': [b'cn=test-users-2,cn=test,ou=ae-dir'],
                                }
                            ),
                         ],
                        5,
                        [],
                    ),
                    (
                        100,
                        [
                            (
                                b'uid=wxrl,cn=test,ou=ae-dir',
                                {
                                    b'cn': [b'Anna Blume'],
                                    b'uid': [b'wxrl'],
                                    b'uidNumber': [b'30027'],
                                    b'memberOf': [
                                        b'cn=test-admins-1,cn=test,ou=ae-dir',
                                        b'cn=test-login-users-1,cn=test,ou=ae-dir',
                                    ],
                                }
                            ),
                         ],
                        5,
                        [],
                    ),
                    (
                        100,
                        [
                            (
                                b'uid=xkcd,cn=test,ou=ae-dir',
                                {
                                    b'cn': [b'Anna Blume'],
                                    b'uid': [b'xkcd'],
                                    b'uidNumber': [b'30028'],
                                    b'memberOf': [b'cn=test-login-users-1,cn=test,ou=ae-dir'],
                                }
                            ),
                         ],
                        5,
                        [],
                    ),
                    (101, [], 5, []),
                )
            )

    def test014_add_aeuser(self):
        with self._get_conn() as aedir_conn:
            uid = 'noob'
            new_entry = aedir_conn.add_aeuser(
                'test',
                'noob',
                'uniqueIdentifier=web2ldap-1489425020.31,cn=people,ou=ae-dir',
                ae_ticket_id='FOOBAR-42',
            )
            self.assertEqual(new_entry['uid'][0], uid)
            self.assertEqual(new_entry['aeTicketId'][0], 'FOOBAR-42')
            with self.assertRaises(ldap0.NO_SUCH_OBJECT) as ctx:
                new_entry = aedir_conn.add_aeuser(
                    'test',
                    'noob',
                    'uniqueIdentifier=foo,cn=bar,ou=ae-dir',
                )
            self.assertEqual(str(ctx.exception), "Could not read aePerson entry 'uniqueIdentifier=foo,cn=bar,ou=ae-dir'")

    def test015_get_role_groups(self):
        with self._get_conn() as aedir_conn:
            role_groups = aedir_conn.get_role_groups(
                'host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
                ('aeVisibleGroups',),
            )
            self.assertEqual(
                role_groups,
                 {
                    'aeVisibleGroups': set([
                        'cn=test-users-2,cn=test,ou=ae-dir',
                        'cn=test-login-users-1,cn=test,ou=ae-dir',
                    ])
                 },
            )

    def test016_get_role_groups_filter(self):
        with self._get_conn() as aedir_conn:
            role_groups_filter = aedir_conn.get_role_groups_filter(
                'host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
                'foo',
                'foo',
            )
            self.assertEqual(role_groups_filter, '')
            role_groups_filter = aedir_conn.get_role_groups_filter(
                'host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
                'memberOf',
                'aeVisibleGroups',
            )
            self.assertTrue(
                (
                    role_groups_filter.startswith('(|(memberOf=cn=')
                    and role_groups_filter.endswith('cn=test,ou=ae-dir))')
                )
            )
            self.assertIn(
                '(memberOf=cn=test-users-2,cn=test,ou=ae-dir)',
                role_groups_filter
            )
            self.assertIn(
                '(memberOf=cn=test-login-users-1,cn=test,ou=ae-dir)',
                role_groups_filter
            )

    def test017_get_sudoers(self):
        with self._get_conn() as aedir_conn:
            self.assertEqual(
                aedir_conn.get_sudoers(
                    'host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
                ),
                [],
            )
            self.assertEqual(
                [
                    (res.dn_b, res.entry_b)
                    for res in aedir_conn.get_sudoers(
                        'host=ae-dir-deb-p1.virtnet1.stroeder.local,cn=ae-dir-provider-hosts,cn=ae,ou=ae-dir',
                        attrlist=None,
                    )
                ],
                [
                    (
                        b'cn=ae-sudo-sys-admins,cn=ae,ou=ae-dir',
                        {
                            b'cn': [b'ae-sudo-sys-admins'],
                            b'description': [b'su - root for AE-DIR system admins'],
                            b'sudoCommand': [b'ALL'],
                            b'sudoUser': [b'%ae-sys-admins'],
                            b'objectClass': [b'top', b'sudoRole', b'aeObject', b'aeSudoRule'],
                            b'sudoHost': [b'ALL'],
                            b'sudoRunAsUser': [b'ALL'],
                        }
                    )
                ],
            )

    def test018_set_password(self):
        with self._get_conn() as aedir_conn:
            # set a known password
            host_dn, host_pw = aedir_conn.set_password(
                'foo.example.com',
                'secretpw',
            )
            self.assertEqual(
                host_dn,
                'host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
            )
            self.assertIsNone(host_pw)
            with self._get_conn(who='host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir', cred=b'secretpw') as ldap_conn:
                self.assertEqual(
                    ldap_conn.whoami_s(),
                    'dn:host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
                )
            # set a auto-generated password
            host_dn, host_pw = aedir_conn.set_password(
                'foo.example.com',
                None,
            )
            self.assertEqual(
                host_dn,
                'host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
            )
            self.assertIsInstance(host_pw, bytes)
            with self._get_conn(who='host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir', cred=host_pw) as ldap_conn:
                self.assertEqual(
                    ldap_conn.whoami_s(),
                    'dn:host=foo.example.com,cn=test-services-1,cn=test,ou=ae-dir',
                )
            # check exceptions
            with self.assertRaises(NoUniqueEntry):
                aedir_conn.set_password(
                    'foobar_does_not_exist',
                    'secretpw',
                )
            with self.assertRaises(NoUniqueEntry):
                aedir_conn.set_password(
                    'foobar',
                    'secretpw',
                    # provoke non-unique name to DN mapping
                    filterstr_tmpl='(|(uid=msin)(uid=ae-dir-pwd))',
                )

    def test019_find_aegroup(self):
        with self._get_conn() as aedir_conn:
            aegroup = aedir_conn.find_aegroup('test-users-2', attrlist=['*'])
            self.assertIsInstance(aegroup, AEGroup)
            self.assertEqual(
                aegroup.dn_s,
                'cn=test-users-2,cn=test,'+self.ae_suffix
            )
            ldap_entry = aegroup.ldap_entry()
            for atype in (
                    'member',
                    'memberUid',
                    'objectClass',
                ):
                if atype in ldap_entry:
                    ldap_entry[atype].sort()
            self.assertEqual(
                ldap_entry,
                {
                    'aeMemberZone': [b'cn=test,ou=ae-dir'],
                    'aeNotBefore': [b'20170116213310Z'],
                    'aeStatus': [b'0'],
                    'cn': [b'test-users-2'],
                    'description': [b'Test group #2'],
                    'gidNumber': [b'30024'],
                    'member': [b'uid=bccb,cn=test,ou=ae-dir', b'uid=luua,cn=test,ou=ae-dir'],
                    'memberUid': [b'bccb', b'luua'],
                    'objectClass': [b'aeGroup', b'aeObject', b'groupOfEntries', b'posixGroup', b'top'],
                }
            )

    def test020_add_aehost(self):
        with self._get_conn() as aedir_conn:
            aedir_conn.add_aehost(
                'foo2.example.net', 'test-services-2',
                entry={
                    'description': ['Testing \xE4\xF6\xFC\xC4\xD6\xDC\xDF...'],
                },
                password='secret123',
            )
            aehost = aedir_conn.find_aehost('foo2.example.net', attrlist=('*', 'pwdPolicySubentry'))
            ldap_entry = aehost.ldap_entry()
            del ldap_entry['userPassword']
            self.assertEqual(
                aehost.dn_s,
                'host=foo2.example.net,cn=test-services-2,cn=test,'+self.ae_suffix,
            )
            ldap_entry['objectClass'].sort()
            self.assertEqual(
                ldap_entry,
                {
                    'aeStatus': [b'0'],
                    'cn': [b'foo2.example.net'],
                    'host': [b'foo2.example.net'],
                    'objectClass': [
                        b'aeDevice',
                        b'aeHost',
                        b'aeObject',
                        b'device',
                        b'ldapPublicKey',
                    ],
                    'description': ['Testing \xE4\xF6\xFC\xC4\xD6\xDC\xDF...'.encode('utf-8')],
                    'pwdPolicySubentry': [b'cn=ppolicy-systems,cn=ae,ou=ae-dir'],
                },
            )
        with self._get_conn(
            who='host=foo2.example.net,cn=test-services-2,cn=test,'+self.ae_suffix,
            cred=b'secret123'
            ) as ldap_conn:
            self.assertEqual(
                ldap_conn.whoami_s(),
                'dn:host=foo2.example.net,cn=test-services-2,cn=test,'+self.ae_suffix,
            )

    def test021_add_aezone(self):
        with self._get_conn() as aedir_conn:
            highest_gid = aedir_conn.find_highest_id(aedir_conn.search_base)
            zone_dn = aedir_conn.add_aezone('test2', 'TICKET-42', 'Zone added for automated testing')
            self.assertEqual(zone_dn, 'cn=test2,ou=ae-dir')
            zone_entries = aedir_conn.search_s(
                zone_dn,
                ldap0.SCOPE_SUBTREE,
                filterstr='(objectClass=*)',
                attrlist=['*'],
            )
        # first compare DN list
        self.assertEqual(
            sorted([ze.dn_b for ze in zone_entries]),
            [
                b'cn=test2,ou=ae-dir',
                b'cn=test2-init,cn=test2,ou=ae-dir',
                b'cn=test2-zone-admins,cn=test2,ou=ae-dir',
                b'cn=test2-zone-auditors,cn=test2,ou=ae-dir',
            ],
        )
        for ze in zone_entries:
            ze.entry_b[b'objectClass'].sort()
        self.assertEqual(
            [ze.entry_b for ze in zone_entries],
            [
                {
                    b'aeStatus': [b'0'],
                    b'aeTag': [b'test2-init'],
                    b'aeTicketId': [b'TICKET-42'],
                    b'cn': [b'test2'],
                    b'description': [b'Zone added for automated testing'],
                    b'objectClass': [
                        b'aeObject',
                        b'aeZone',
                        b'namedObject',
                    ],
                    b'aeZoneAdmins': [b'cn=test2-zone-admins,cn=test2,ou=ae-dir'],
                    b'aeZoneAuditors': [b'cn=test2-zone-auditors,cn=test2,ou=ae-dir'],
                },
                {
                    b'aeStatus': [b'0'],
                    b'cn': [b'test2-init'],
                    b'description': [b"Initialization of zone 'test2'"],
                    b'objectClass': [b'aeTag', b'namedObject'],
                },
                {
                    b'aeStatus': [b'0'],
                    b'aeTag': [b'test2-init'],
                    b'aeTicketId': [b'TICKET-42'],
                    b'cn': [b'test2-zone-admins'],
                    b'description': [b"Group members are zone admins who can manage zone 'test2'"],
                    b'gidNumber': [('%d' % (highest_gid+1)).encode('ascii')],
                    b'objectClass': [
                        b'aeGroup',
                        b'aeObject',
                        b'groupOfEntries',
                        b'posixGroup',
                    ],
                },
                {
                    b'aeStatus': [b'0'],
                    b'aeTag': [b'test2-init'],
                    b'aeTicketId': [b'TICKET-42'],
                    b'cn': [b'test2-zone-auditors'],
                    b'description': [b"Group members are zone auditors who can read zone 'test2'"],
                    b'gidNumber': [('%d' % (highest_gid+2)).encode('ascii')],
                    b'objectClass': [
                        b'aeGroup',
                        b'aeObject',
                        b'groupOfEntries',
                        b'posixGroup',
                    ],
                },
            ]
        )

    def test022_starttls_anon(self):
        server = list(self.servers.values())[0]
        with self.ldap_object_class(
                server.ldap_uri,
                who='',
                cred=b'',
                cacert_filename='tests/tls/ca-chain.pem',
            ) as anon_aedir_conn:
            self.assertEqual(anon_aedir_conn.whoami_s(), '')

    def test023_starttls_client_cert(self):
        server = list(self.servers.values())[0]
        with self.ldap_object_class(
                server.ldap_uri,
                cacert_filename='tests/tls/ca-chain.pem',
                client_cert_filename='tests/tls/test-client.crt',
                client_key_filename='tests/tls/test-client.key',
            ) as aedir_conn:
            aedir_conn.sasl_non_interactive_bind_s('EXTERNAL')
            self.assertEqual(aedir_conn.whoami_s(), 'dn:uid=test-client,cn=test,ou=ae-dir')


if __name__ == '__main__':
    unittest.main()
