# -*- coding: ascii -*-
"""
aedir.models - classes for various \xC6-DIR objects

See https://ae-dir.com/python.html for details.

(c) 2016-2021 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import enum
from datetime import datetime
from typing import Optional, Union

from ldap0.base import decode_list
from ldap0.functions import str2datetime, datetime2str
from ldap0.dn import DNObj
from ldap0.typehints import BytesList, EntryMixed

# exported symbols
__all__ = [
    'AEBaseModel',
    'AEGroup',
    'AEHost',
    'AEObject',
    'AEPerson',
    'AEService',
    'AESrvGroup',
    'AEStatus',
    'AETag',
    'AEUser',
    'AEZone',
]


class AEStatus(enum.IntEnum):
    """
    Enum class for attribute aeStatus
    """
    registered = -1
    active = 0
    deactivated = 1
    archived = 2

    @classmethod
    def from_str(cls, val: str):
        """
        create instance from str
        """
        return cls(int(val))

    def __str__(self) -> str:
        return str(self.value)

    def __bytes__(self) -> bytes:
        return str(self.value).encode('ascii')

    def encode(self, encoding='ascii') -> bytes:
        """
        returns aeStatus attribute value as encoded bytes
        """
        return str(self.value).encode(encoding)


# map for all attribute values which shall not be str
NATIVE_TYPE_FUNC = {
    'aeABAccessGroups': DNObj.from_str,
    'aeDept': DNObj.from_str,
    'aeDisplayNameGroups': DNObj.from_str,
    'aeGroupReference': DNObj.from_str,
    'aeHost': DNObj.from_str,
    'aeLocation': DNObj.from_str,
    'aeLoginGroups': DNObj.from_str,
    'aeLogStoreGroups': DNObj.from_str,
    'aeMemberZone': DNObj.from_str,
    'aeNotAfter': str2datetime,
    'aeNotBefore': str2datetime,
    'aeNwDevice': DNObj.from_str,
    'aeOwner': DNObj.from_str,
    'aePasswordAdmins': DNObj.from_str,
    'aePerson': DNObj.from_str,
    'aeProxyFor': DNObj.from_str,
    'aeRequires': DNObj.from_str,
    'aeRoot': DNObj.from_str,
    'aeSetupGroups': DNObj.from_str,
    'aeSrvGroup': DNObj.from_str,
    'aeStatus': AEStatus.from_str,
    'aeVisibleGroups': DNObj.from_str,
    'aeVisibleSudoers': DNObj.from_str,
    'aeZoneAdmins': DNObj.from_str,
    'aeZoneAuditors': DNObj.from_str,
    'defaultNamingContext': DNObj.from_str,
    'gidNumber': int,
    'manager': DNObj.from_str,
    'member': DNObj.from_str,
    'oathHOTPToken': DNObj.from_str,
    'oathTOTPToken': DNObj.from_str,
    'pwdPolicySubentry': DNObj.from_str,
    'seeAlso': DNObj.from_str,
    'uidNumber': int,
    'userCertificate': bytes,
    'userPKCS12': bytes,
}

# attribute types declared with SINGLE-VALUE or similar constraint
SINGLE_VALUE = {
    'aeNotAfter',
    'aeNotBefore',
    'aeStatus',
    'aeTicketId',
    'cn',
    'departmentNumber',
    'description',
    'employeeNumber',
    'gidNumber',
    'givenName',
    'mail',
    'o',
    'ou',
    'pwdPolicySubentry',
    'sn',
    'uid',
    'uidNumber',
    'uniqueIdentifier',
    'userPassword',
}


class AEBaseModel:
    """
    Managed object (see abstract object class aeObject)
    """
    structural_object_class = None
    __must__ = frozenset((
        'objectClass',
    ))
    __may__ = frozenset()
    __rdn_attr__ = None
    __object_classes__ = (())
    __ignored_attrs__ = frozenset()
    __slots__ = (
        '_rdn_attr',
        '_parent_dn',
    ) + tuple(__must__) + tuple(__may__)

    def __init__(
            self,
            parent_dn: Optional[Union[DNObj, str]] = None,
            rdn_attr: str = None,
            **attrs,
        ):
        self.objectClass = None
        if 'objectClass' not in attrs:
            attrs['objectClass'] = self.__object_classes__
        for atype in self.__must__:
            # provoke KeyError for mandatory but non-existent attributes
            setattr(self, atype, attrs[atype])
        for atype in self.__may__:
            if atype in attrs:
                setattr(self, atype, attrs[atype])
            else:
                setattr(self, atype, None)
        if not isinstance(self.objectClass, set):
            self.objectClass = set(self.objectClass)
        unknown_attrs = set(attrs.keys()) - (self.__must__ | self.__may__)
        if unknown_attrs:
            raise AttributeError('Unknown attributes passed in: %r' % (sorted(unknown_attrs),))
        if rdn_attr is None:
            self._rdn_attr = self.__rdn_attr__
        else:
            self._rdn_attr = rdn_attr
        self.parent_dn = parent_dn

    @property
    def parent_dn(self) -> DNObj:
        """
        returns the distinguished name of parent entry as DNObj
        """
        return self._parent_dn

    @parent_dn.setter
    def parent_dn(
            self,
            parent_dn: Union[DNObj, str],
        ) -> DNObj:
        """
        returns the distinguished name of parent entry as DNObj
        """
        if parent_dn is None:
            self._parent_dn = None
            return
        if isinstance(parent_dn, str):
            self._parent_dn = DNObj.from_str(parent_dn)
        elif isinstance(parent_dn, DNObj):
            self._parent_dn = parent_dn
        else:
            raise TypeError('Argument parent_dn has wrong type: %r' % (parent_dn,))

    @property
    def dn_o(self) -> DNObj:
        """
        return the full distinguished name as DNObj
        """
        if self._parent_dn is None:
            raise ValueError('No parent DN set')
        return DNObj((((self._rdn_attr, self._ldap_rdn_value),),)) + self.parent_dn

    @property
    def dn_s(self) -> str:
        """
        return the full distinguished name as str
        """
        return str(self.dn_o)

    @staticmethod
    def _class_attr_value(atype, avalues):
        pytype = NATIVE_TYPE_FUNC.get(atype, str)
        if pytype != bytes:
            avalues = decode_list(avalues, encoding='utf-8')
        avalues = [pytype(aval) for aval in avalues]
        res = avalues
        if atype in SINGLE_VALUE:
            res = avalues[0]
        return res

    @classmethod
    def from_dict(
            cls,
            entry: EntryMixed,
            parent_dn: Optional[Union[DNObj, str]] = None,
        ):
        """
        create AEObject instance from dict representation of an LDAP entry
        """
        attrs = {
            atype: cls._class_attr_value(atype, entry[atype])
            for atype, avalues in entry.items()
            if not atype in cls.__ignored_attrs__
        }
        return cls(parent_dn, **attrs)

    @classmethod
    def from_search_result(cls, res):
        """
        create AEObject instance from ldap0.res.SearchResultEntry
        """
        return cls.from_dict(res.entry_as, res.dn_o.parent())

    @property
    def _ldap_rdn_value(self):
        """
        construct the attribute value to be used for characteristic
        attribute in RDN
        """
        aval = getattr(self, self._rdn_attr)
        if isinstance(aval, list):
            aval = aval[0]
        if isinstance(aval, datetime):
            aval = datetime2str(aval)
        elif isinstance(aval, int):
            aval = str(aval)
        elif not isinstance(aval, str):
            raise TypeError('Unsupported type %r for building RDN' % (type(aval),))
        return aval

    def _ldap_entry_values(self, atype) -> BytesList:
        """
        returns list of encoded bytes values to be used in LDAP entry
        """
        avalue = getattr(self, atype)
        if isinstance(avalue, DNObj):
            avalues = [avalue]
        elif isinstance(avalue, (list, tuple, set)):
            avalues = avalue
        else:
            avalues = [avalue]
        res = []
        for aval in avalues:
            if isinstance(aval, datetime):
                aval = datetime2str(aval).encode('utf-8')
            elif isinstance(aval, str):
                aval = aval.encode('utf-8')
            elif isinstance(aval, (AEStatus, DNObj)):
                aval = aval.encode('utf-8')
            elif isinstance(aval, int):
                aval = str(aval).encode('ascii')
            elif isinstance(aval, bool):
                aval = str(aval).upper().encode('utf-8')
            elif not isinstance(aval, bytes):
                raise TypeError('Attribute %r has unsupported type %r' % (atype, aval))
            res.append(aval)
        return res

    def ldap_entry(self) -> EntryMixed:
        """
        returns LDAP entry as dictionary to be used with
        LDAPObject.add() and friends
        """
        res = {}
        for atype in self.__must__:
            if getattr(self, atype) is None:
                raise ValueError('No attribute value set for %r' % (atype,))
            res[atype] = self._ldap_entry_values(atype)
        for atype in self.__may__:
            if getattr(self, atype) is not None:
                res[atype] = self._ldap_entry_values(atype)
        return res


class AEObject(AEBaseModel):
    """
    Managed object (see abstract object class aeObject)
    """
    structural_object_class = 'aeObject'
    __must__ = AEBaseModel.__must__ | frozenset((
        'aeStatus',
    ))
    __may__ = AEBaseModel.__may__ | frozenset((
        'aeExpiryStatus',
        'aeNotAfter',
        'aeNotBefore',
        'aeTag',
        'aeTicketId',
        'description',
    ))
    __rdn_attr__ = 'cn'
    __object_classes__ = (structural_object_class,)
    __slots__ = tuple(__must__) + tuple(__may__)


class AETag(AEBaseModel):
    """
    Tag object
    """
    structural_object_class = 'aeTag'
    __object_classes__ = (
        'namedObject',
        structural_object_class,
    )
    __rdn_attr__ = 'cn'
    __must__ = AEBaseModel.__must__ | frozenset((
        'aeStatus',
        'cn',
        'description',
    ))
    __may__ = frozenset()
    __slots__ = tuple(__must__) + tuple(__may__)


class AEZone(AEObject):
    """
    Zone object
    """
    structural_object_class = 'aeZone'
    __object_classes__ = (
        'namedObject',
        'aeObject',
        structural_object_class,
    )
    __rdn_attr__ = 'cn'
    __must__ = AEObject.__must__ | frozenset((
        'cn',
        'description',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeABAccessGroups',
        'aeChildClasses',
        'aeDept',
        'aeLocation',
        'aePasswordAdmins',
        'aeTag',
        'aeTicketId',
        'aeZoneAdmins',
        'aeZoneAuditors',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)


class AEPerson(AEObject):
    """
    Person object
    """
    structural_object_class = 'aePerson'
    __object_classes__ = (
        'person',
        'organizationalPerson',
        'inetOrgPerson',
        structural_object_class,
        'aeObject',
        'msPerson',
    )
    __rdn_attr__ = 'uniqueIdentifier'
    __must__ = AEObject.__must__ | frozenset((
        'cn',
        'sn',
        'givenName',
        'aeDept',
        'aeLocation',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeSourceUri',
        'businessCategory',
        'c',
        'departmentNumber',
        'displayName',
        'employeeNumber',
        'employeeType',
        'facsimileTelephoneNumber',
        'homePhone',
        'jpegPhoto',
        'l',
        'labeledURI',
        'mail',
        'manager',
        'mobile',
        'o',
        'ou',
        'postalAddress',
        'postalCode',
        'postOfficeBox',
        'preferredLanguage',
        'roomNumber',
        'st',
        'street',
        'telephoneNumber',
        'title',
        'uniqueIdentifier',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)


class AEService(AEObject):
    """
    Personal user account object
    """
    structural_object_class = 'aeService'
    __object_classes__ = (
        'account',
        'aeObject',
        structural_object_class,
        'posixAccount',
        'aeSSHAccount',
    )
    __rdn_attr__ = 'uid'
    __must__ = AEObject.__must__ | frozenset((
        __rdn_attr__,
        'cn',
        'gidNumber',
        'homeDirectory',
        'uidNumber',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeHost',
        'aeSrvGroup',
        'aeRemoteHost',
        'aeSSHPermissions',
        'loginShell',
        'sshPublicKey',
        'userCertificate',
        'pwdPolicySubentry',
        'userPassword',
        'seeAlso',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)

    def __init__(
            self,
            parent_dn: Optional[Union[DNObj, str]] = None,
            rdn_attr: str = None,
            **attrs,
        ):
        if 'cn' not in attrs:
            attrs['cn'] = attrs['uid']
        super().__init__(
            parent_dn=parent_dn,
            rdn_attr=rdn_attr,
            **attrs,
        )


class AEUser(AEObject):
    """
    Personal user account object
    """
    structural_object_class = 'aeUser'
    __object_classes__ = (
        'account',
        'person',
        'organizationalPerson',
        'inetOrgPerson',
        'aeObject',
        structural_object_class,
        'posixAccount',
        'aeSSHAccount',
    )
    __rdn_attr__ = 'uid'
    __must__ = AEObject.__must__ | frozenset((
        __rdn_attr__,
        'aePerson',
        'cn',
        'displayName',
        'gidNumber',
        'givenName',
        'homeDirectory',
        'sn',
        'uidNumber',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeRemoteHost',
        'aeSSHPermissions',
        'loginShell',
        'mail',
        'sshPublicKey',
        'userCertificate',
        'pwdPolicySubentry',
        'userPassword',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)


class AEHost(AEObject):
    """
    Host object
    """
    structural_object_class = 'aeHost'
    __object_classes__ = (
        'device',
        'aeDevice',
        'aeObject',
        structural_object_class,
        'ldapPublicKey',
    )
    __rdn_attr__ = 'host'
    __must__ = AEObject.__must__ | frozenset((
        __rdn_attr__,
        'cn',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeHwSerialNumber',
        'aeLocation',
        'aeOwner',
        'aeRemoteHost',
        'aeSrvGroup',
        'aeStockId',
        'displayName',
        'l',
        'serialNumber'
        'sshPublicKey',
        'pwdPolicySubentry',
        'userPassword',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)


class AEGroup(AEObject):
    """
    Group object
    """
    structural_object_class = 'aeGroup'
    __object_classes__ = (
        structural_object_class,
        'groupOfEntries',
        'posixGroup',
        'aeObject',
    )
    __ignored_attrs__ = frozenset(('memberUid',))
    __rdn_attr__ = 'cn'
    __must__ = AEObject.__must__ | frozenset((
        __rdn_attr__,
        'gidNumber',
        'description',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeDept',
        'aeLocation',
        'aeMemberZone',
        'displayName',
        'member',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)

    def ldap_entry(self) -> EntryMixed:
        """
        returns LDAP entry as dictionary to be used with
        LDAPObject.add() and friends
        """
        res = super().ldap_entry()
        if self.member:
            res['memberUid'] = [
                dn[4:].split(b',')[0]
                for dn in res.get('member', [])
            ]
        return res


class AESrvGroup(AEObject):
    """
    Service group object
    """
    structural_object_class = 'aeSrvGroup'
    __object_classes__ = (
        structural_object_class,
        'aeObject',
    )
    __rdn_attr__ = 'cn'
    __must__ = AEObject.__must__ | frozenset((
        __rdn_attr__,
        'description',
    ))
    __may__ = AEObject.__may__ | frozenset((
        'aeDisplayNameGroups',
        'aeFqdn',
        'aeLoginGroups',
        'aeLogStoreGroups',
        'aeLogStorePeriod',
        'aeProxyFor',
        'aeRequires',
        'aeSetupGroups',
        'aeSSHProxyCommand',
        'aeVisibleGroups',
        'aeVisibleSudoers',
    )) - __must__
    __slots__ = tuple(__must__) + tuple(__may__)
