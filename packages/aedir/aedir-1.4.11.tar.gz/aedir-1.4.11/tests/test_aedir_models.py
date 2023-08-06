# -*- coding: ascii -*-
"""
Automatic tests for module aedir.models
"""

import unittest
from datetime import datetime

from ldap0.dn import DNObj

from aedir.models import (
    AEGroup,
    AEHost,
    AEObject,
    AEPerson,
    AEService,
    AESrvGroup,
    AEStatus,
    AETag,
    AEUser,
    AEZone,
)


class Test001AEStatus(unittest.TestCase):
    """
    test enum class AEStatus
    """
    maxDiff = None

    def test_ae_status(self):
        ae_status = AEStatus(0)
        self.assertEqual(ae_status, 0)
        self.assertEqual(ae_status, AEStatus.active)
        self.assertEqual(int(ae_status), 0)
        self.assertEqual(str(ae_status), '0')
        self.assertEqual(bytes(ae_status), b'0')
        self.assertEqual(ae_status.encode(), b'0')
        self.assertEqual(ae_status.encode('utf-16-le'), b'0\x00')
        with self.assertRaises(ValueError):
            ae_status = AEStatus(-2)
        with self.assertRaises(ValueError):
            ae_status = AEStatus(99)


class Test002AEObject(unittest.TestCase):
    """
    test class AEObject
    """
    maxDiff = None

    def test_ae_object(self):
        ae_object_entry = {
            'objectClass': [b'aeObject'],
            'aeStatus': [b'0'],
            'aeNotBefore': [b'19700101000000Z'],
        }
        ae_object = AEObject(
            parent_dn='cn=test,ou=ae-dir',
            aeStatus=0,
            aeNotBefore=datetime(1970, 1, 1, 0, 0, 0),
        )
        self.assertEqual(ae_object.objectClass, {'aeObject'})
        self.assertEqual(ae_object.aeStatus, 0)
        self.assertEqual(ae_object.aeNotBefore, datetime(1970, 1, 1, 0, 0, 0))
        self.assertEqual(ae_object.ldap_entry(), ae_object_entry)
        ae_object = AEObject.from_dict(ae_object_entry)
        self.assertEqual(ae_object.objectClass, {'aeObject'})
        self.assertEqual(ae_object.aeStatus, 0)
        self.assertEqual(ae_object.aeNotBefore, datetime(1970, 1, 1, 0, 0, 0))
        self.assertEqual(ae_object.ldap_entry(), ae_object_entry)
        with self.assertRaises(AttributeError):
            ae_object.foobar = 'foo'
        with self.assertRaises(AttributeError) as attr_error:
            AEObject(
                objectClass=['aeObject',],
                aeStatus=0,
                aeNotBefore=datetime(1970, 1, 1, 0, 0, 0),
                foo='foo',
                bar='bar',
            )
        self.assertEqual(str(attr_error.exception), "Unknown attributes passed in: ['bar', 'foo']")
        with self.assertRaises(KeyError):
            AEObject()
        with self.assertRaises(KeyError):
            AEObject.from_dict({})
        with self.assertRaises(KeyError):
            AEObject(objectClass=['aeObject'])
        ae_object = AEObject(
            aeStatus=None,
            aeNotBefore=datetime(1970, 1, 1, 0, 0, 0),
        )
        with self.assertRaises(ValueError) as val_error:
            _ = ae_object.ldap_entry()
        self.assertEqual(str(val_error.exception), "No attribute value set for 'aeStatus'")
        with self.assertRaises(TypeError) as type_error:
            ae_object = AEObject(
                parent_dn=b'cn=test,ou=ae-dir',
                aeStatus=0,
            )
        self.assertEqual(
            str(type_error.exception),
            "Argument parent_dn has wrong type: b'cn=test,ou=ae-dir'"
        )


class Test003AEPerson(unittest.TestCase):
    """
    test class AEPerson
    """
    maxDiff = None

    def test_ae_person(self):
        ae_person_entry = {
            'objectClass': [
                b'aeObject',
                b'aePerson',
                b'inetOrgPerson',
                b'organizationalPerson',
                b'person',
            ],
            'cn': [b'Fred Feuerstein'],
            'sn': [b'Feuerstein'],
            'givenName': [b'Fred'],
            'aeDept': [b'departmentNumber=0,cn=people,ou=ae-dir'],
            'aeLocation': [b'cn=no-location,cn=people,ou=ae-dir'],
            'aeStatus': [b'0'],
            'aeNotBefore': [b'19700101000000Z'],
            'aeNotAfter': [b'19700131000000Z'],
            'uniqueIdentifier': [b'hr-0815'],
            'employeeNumber': [b'123456'],
        }
        ae_person = AEPerson.from_dict(
            ae_person_entry,
            parent_dn=DNObj.from_str('cn=people,dc=ae-dir,dc=example,dc=org'),
        )
        self.assertEqual(
            ae_person.dn_s,
            'uniqueIdentifier=hr-0815,cn=people,dc=ae-dir,dc=example,dc=org'
        )
        self.assertEqual(
            ae_person.objectClass,
            {
                'person',
                'organizationalPerson',
                'inetOrgPerson',
                'aePerson',
                'aeObject',
            }
        )
        self.assertEqual(ae_person.cn, 'Fred Feuerstein')
        self.assertEqual(ae_person.sn, 'Feuerstein')
        self.assertEqual(ae_person.givenName, 'Fred')
        self.assertEqual(ae_person.aeStatus, 0)
        self.assertEqual(ae_person.aeNotBefore, datetime(1970, 1, 1, 0, 0, 0))
        ae_person_ldap_entry = ae_person.ldap_entry()
        ae_person_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_person_ldap_entry, ae_person_entry)
        with self.assertRaises(AttributeError):
            ae_person.foobar = 'foo'


class Test004AEUser(unittest.TestCase):
    """
    test class AEUser
    """
    maxDiff = None

    def test_ae_user(self):
        ae_user_entry = {
            'objectClass': [
                b'account',
                b'aeObject',
                b'aeSSHAccount',
                b'aeUser',
                b'inetOrgPerson',
                b'organizationalPerson',
                b'person',
                b'posixAccount',
            ],
            'uid': [b'xkcd'],
            'uidNumber': [b'12345'],
            'gidNumber': [b'12345'],
            'aePerson': [b'uniqueIdentifier=42,cn=people,ou=ae-dir'],
            'aeStatus': [b'0'],
            'aeNotBefore': [b'19700101000000Z'],
            'cn': [b'Fred Feuerstein'],
            'sn': [b'Feuerstein'],
            'displayName': [b'Fred Feuerstein (xkcd/12345)'],
            'givenName': [b'Fred'],
            'homeDirectory': [b'/home/xkcd'],
            'mail': [b'xkcd@example.com'],
            'pwdPolicySubentry': [b'cn=ppolicy-users,cn=ae,ou=ae-dir'],
        }
        ae_user = AEUser(
            parent_dn=DNObj.from_str('cn=test,ou=ae-dir'),
            uid='xkcd',
            uidNumber=12345,
            gidNumber=12345,
            aePerson=DNObj.from_str('uniqueIdentifier=42,cn=people,ou=ae-dir'),
            aeStatus=0,
            aeNotBefore=datetime(1970, 1, 1, 0, 0, 0),
            cn='Fred Feuerstein',
            sn='Feuerstein',
            givenName='Fred',
            displayName='Fred Feuerstein (xkcd/12345)',
            mail='xkcd@example.com',
            homeDirectory='/home/xkcd',
            pwdPolicySubentry='cn=ppolicy-users,cn=ae,ou=ae-dir',
        )
        self.assertEqual(ae_user._ldap_rdn_value, 'xkcd')
        self.assertEqual(ae_user.dn_s, 'uid=xkcd,cn=test,ou=ae-dir')
        self.assertEqual(
            ae_user.objectClass,
            {
                'account',
                'person',
                'organizationalPerson',
                'inetOrgPerson',
                'aeObject',
                'aeSSHAccount',
                'aeUser',
                'posixAccount',
            }
        )
        self.assertEqual(ae_user.uid, 'xkcd')
        self.assertEqual(ae_user.uidNumber, 12345)
        self.assertEqual(ae_user.aeStatus, 0)
        self.assertEqual(ae_user.aeNotBefore, datetime(1970, 1, 1, 0, 0, 0))
        self.assertEqual(
            ae_user.aePerson,
            DNObj.from_str('uniqueIdentifier=42,cn=people,ou=ae-dir')
        )
        ae_user_ldap_entry = ae_user.ldap_entry()
        ae_user_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_user_ldap_entry, ae_user_entry)
        ae_user = AEUser.from_dict(
            ae_user_entry,
            parent_dn=DNObj.from_str('cn=test,ou=ae-dir'),
        )
        self.assertEqual(
            ae_user.objectClass,
            {
                'account',
                'person',
                'organizationalPerson',
                'inetOrgPerson',
                'aeObject',
                'aeUser',
                'posixAccount',
                'aeSSHAccount',
            }
        )
        self.assertEqual(ae_user.uid, 'xkcd')
        self.assertEqual(ae_user.aeStatus, 0)
        self.assertEqual(ae_user.aeNotBefore, datetime(1970, 1, 1, 0, 0, 0))
        ae_user_ldap_entry = ae_user.ldap_entry()
        ae_user_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_user_ldap_entry, ae_user_entry)
        with self.assertRaises(AttributeError):
            ae_user.foobar = 'foo'


class Test005AEHost(unittest.TestCase):
    """
    test class AEHost
    """
    maxDiff = None

    def test_ae_host(self):
        ae_host_entry = {
            'aeStatus': [b'-1'],
            'cn': [b'host1'],
            'host': [b'host1.example.com'],
            'objectClass': [
                b'aeDevice',
                b'aeHost',
                b'aeObject',
                b'device',
                b'ldapPublicKey',
            ],
            'pwdPolicySubentry': [b'cn=dummy'],
        }
        ae_host = AEHost(
            cn='host1',
            host='host1.example.com',
            aeStatus=-1,
            pwdPolicySubentry='cn=dummy',
        )
        ae_host_ldap_entry = ae_host.ldap_entry()
        ae_host_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_host_ldap_entry, ae_host_entry)


class Test006AEGroup(unittest.TestCase):
    """
    test class AEGroup
    """
    maxDiff = None

    def test_ae_group(self):
        ae_group_entry = {
            'aeStatus': [b'0'],
            'cn': [b'test-users-1'],
            'gidNumber': [b'12345'],
            'description': [b'Test users #1'],
            'objectClass': [
                b'aeGroup',
                b'aeObject',
                b'groupOfEntries',
                b'posixGroup',
            ],
            'member': [
                b'uid=xkcd,cn=test,ou=ae-dir',
                b'uid=fred,cn=test,ou=ae-dir',
            ],
            'memberUid': [b'xkcd', b'fred'],
        }
        ae_group = AEGroup(
            cn='test-users-1',
            gidNumber=12345,
            aeStatus=AEStatus.active,
            description='Test users #1',
        )
        ae_group.member = [
            DNObj.from_str('uid=xkcd,cn=test,ou=ae-dir'),
            DNObj.from_str('uid=fred,cn=test,ou=ae-dir'),
        ]
        self.assertEqual(ae_group.aeStatus, 0)
        ae_group_ldap_entry = ae_group.ldap_entry()
        ae_group_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_group_ldap_entry, ae_group_entry)


class Test007AEService(unittest.TestCase):
    """
    test class AEHost
    """
    maxDiff = None

    def test_ae_service(self):
        ae_service_entry = {
            'aeStatus': [b'0'],
            'uid': [b'system_user1'],
            'cn': [b'system_user1'],
            'objectClass': [
                b'account',
                b'aeObject',
                b'aeSSHAccount',
                b'aeService',
                b'posixAccount',
            ],
            'uidNumber': [b'12345'],
            'gidNumber': [b'12345'],
            'pwdPolicySubentry': [b'cn=dummy'],
            'homeDirectory': [b'/home/system_user1'],
        }
        ae_service = AEService(
            uid='system_user1',
            aeStatus=0,
            uidNumber=12345,
            gidNumber=12345,
            homeDirectory='/home/system_user1',
            pwdPolicySubentry='cn=dummy',
        )
        ae_service_ldap_entry = ae_service.ldap_entry()
        ae_service_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_service_ldap_entry, ae_service_entry)


class Test008AEZone(unittest.TestCase):
    """
    test class AEHost
    """
    maxDiff = None

    def test_ae_zone(self):
        ae_zone_entry =   {'aeStatus': [b'0'],
            'cn': [b'dangerzone'],
            'description': [b'Dangerous stuff inside'],
            'objectClass': [b'aeObject', b'aeZone', b'namedObject']
        }
        ae_zone = AEZone(
            cn='dangerzone',
            aeStatus=0,
            description='Dangerous stuff inside',
        )
        ae_zone_ldap_entry = ae_zone.ldap_entry()
        ae_zone_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_zone_ldap_entry, ae_zone_entry)


class Test009AETag(unittest.TestCase):
    """
    test class AEHost
    """
    maxDiff = None

    def test_ae_tag(self):
        ae_tag_entry =   {
            'objectClass': [b'aeTag', b'namedObject'],
            'aeStatus': [b'2'],
            'cn': [b'some-info'],
            'description': [b'Some information'],
        }
        ae_tag = AETag(
            cn='some-info',
            aeStatus=AEStatus.archived,
            description='Some information',
        )
        ae_tag_ldap_entry = ae_tag.ldap_entry()
        ae_tag_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_tag_ldap_entry, ae_tag_entry)


class Test010AESrvGroup(unittest.TestCase):
    """
    test class AEGroup
    """
    maxDiff = None

    def test_ae_srv_group(self):
        ae_srv_group_entry = {
            'aeStatus': [b'0'],
            'cn': [b'test-services-1'],
            'description': [b'Test services #1'],
            'objectClass': [
                b'aeObject',
                b'aeSrvGroup',
            ],
            'aeLogStoreGroups': [b'cn=sys-admins,cn=example,ou=ae-dir'],
            'aeLoginGroups': [b'cn=sys-admins,cn=example,ou=ae-dir'],
            'aeSetupGroups': [b'cn=sys-admins,cn=example,ou=ae-dir'],
            'aeTag': [b'test-any-tag'],
            'aeTicketId': [b'IAM-42'],
            'aeVisibleGroups': [b'cn=sys-admins,cn=example,ou=ae-dir'],
            'aeVisibleSudoers': [b'cn=sudo-sys-admins,cn=example,ou=ae-dir'],
        }
        ae_srv_group = AESrvGroup(
            cn='test-services-1',
            aeStatus=AEStatus.active,
            description='Test services #1',
            aeLogStoreGroups=[DNObj.from_str('cn=sys-admins,cn=example,ou=ae-dir')],
            aeLoginGroups=[DNObj.from_str('cn=sys-admins,cn=example,ou=ae-dir')],
            aeSetupGroups=[DNObj.from_str('cn=sys-admins,cn=example,ou=ae-dir')],
            aeTag=['test-any-tag'],
            aeTicketId='IAM-42',
            aeVisibleGroups=[DNObj.from_str('cn=sys-admins,cn=example,ou=ae-dir')],
            aeVisibleSudoers=[DNObj.from_str('cn=sudo-sys-admins,cn=example,ou=ae-dir')],
        )
        self.assertEqual(ae_srv_group.aeStatus, 0)
        ae_srv_group_ldap_entry = ae_srv_group.ldap_entry()
        ae_srv_group_ldap_entry['objectClass'].sort()
        self.assertEqual(ae_srv_group_ldap_entry, ae_srv_group_entry)


if __name__ == '__main__':
    unittest.main()
