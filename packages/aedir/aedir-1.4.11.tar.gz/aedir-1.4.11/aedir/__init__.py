# -*- coding: ascii -*-
"""
aedir - Generic classes and functions for dealing with AE-DIR

See https://ae-dir.com/python.html for details.

(c) 2016-2021 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

# Imports from Python's standard lib
import random
import time
import sys
import os
import string
import logging
import logging.handlers
import logging.config
from typing import Dict, Iterator, List, Optional, Sequence, Set, Tuple, Union

# Imports from ldap0 module package
import ldap0
import ldap0.sasl
import ldap0.controls
import ldap0.modlist
from ldap0.functions import escape_format
from ldap0.base import encode_list, decode_list, encode_entry_dict, decode_entry_dict
from ldap0.dn import escape_str as escape_dn_str
from ldap0.dn import DNObj
from ldap0.filter import escape_str as escape_filter_str
from ldap0.filter import map_filter_parts, compose_filter
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.controls.simple import AuthorizationIdentityRequestControl
from ldap0.controls.readentry import PreReadControl, PostReadControl
from ldap0.controls.deref import DereferenceControl
from ldap0.controls.sss import SSSRequestControl
from ldap0.ldapurl import LDAPUrl
from ldap0.pw import random_string
from ldap0.typehints import EntryStr, AttrList, StrList
from ldap0.res import LDAPResult

from .__about__ import __version__, __author__, __license__
from .models import (
    AEGroup,
    AEHost,
    AESrvGroup,
    AEStatus,
    AETag,
    AEUser,
    AEZone,
)


# exported symbols
__all__ = [
    'AEDirUrl',
    'AEDirObject',
    'AEDIR_SEARCH_BASE',
    'aedir_aehost_dn',
    'aedir_aeuser_dn',
    'extract_zone',
    'init_logger',
    'members2uids',
]

# Timeout in seconds when connecting to local and remote LDAP servers
# used for ldap0.OPT_NETWORK_TIMEOUT and ldap0.OPT_TIMEOUT
LDAP_TIMEOUT = 4.0

# Number of times connecting to LDAP is tried
LDAP_MAXRETRYCOUNT = 2
LDAP_RETRYDELAY = 2.0

# Default search base for AE-DIR
AEDIR_SEARCH_BASE = 'ou=ae-dir'

AESRVGROUP_GROUPREF_ATTRS = [
    'aeDisplayNameGroups',
    'aeSetupGroups',
    'aeLogStoreGroups',
    'aeLoginGroups',
    'aeVisibleGroups',
    'aeVisibleSudoers',
]

AE_SUDOERS_ATTRS = [
    'cn', 'objectClass', 'description',
    'sudoCommand',
    'sudoHost',
    'sudoNotAfter', 'sudoNotBefore',
    'sudoOption', 'sudoOrder',
    'sudoRunAs', 'sudoRunAsGroup', 'sudoRunAsUser', 'sudoUser',
]

# filter template for locating any active entity by name which authenticates
# (e.g. with password)
AUTHC_ENTITY_FILTER_TMPL = (
    '(&'
      '(|'
        '(&'
          '(|(objectClass=aeUser)(objectClass=aeService))'
          '(uid={0})'
        ')'
        '(&'
          '(objectClass=aeHost)'
          '(host={0})'
        ')'
      ')'
      '(aeStatus=0)'
    ')'
)

# default length for generated passwords
PWD_LENGTH = 40

# alphabet used  for generated passwords
PWD_ALPHABET = string.ascii_letters + string.digits

# where to find the logging config file
AE_LOGGING_CONFIG = os.environ.get('AE_LOGGING_CONFIG', '/opt/ae-dir/etc/ae-logging.conf')


def extract_zone(
        ae_object_dn: str,
        aeroot_dn: str = AEDIR_SEARCH_BASE,
    ) -> str:
    """
    return the extracted zone name from dn
    """
    asserted_suffix = ','+aeroot_dn.lower()
    if not ae_object_dn.lower().endswith(asserted_suffix):
        raise ValueError(
            '%r does not end with %r' % (ae_object_dn, asserted_suffix)
        )
    dn_with_base = DNObj.from_str(ae_object_dn[0:-len(aeroot_dn)-1])
    assert dn_with_base[-1][0][0] == 'cn', ValueError(
        'Expected zone attribute to be cn, got %r' % (dn_with_base[-1][0],)
    )
    return dn_with_base[-1][0][1]


def aedir_aeuser_dn(
        uid: str,
        zone: Optional[str] = None,
        aeroot_dn: str = AEDIR_SEARCH_BASE,
    ) -> str:
    """
    Returns a bind DN of a aeUser entry
    """
    if not zone:
        try:
            uid, zone = uid.split('@', 1)
        except ValueError:
            pass
    if zone:
        first_dn_part = ldap0.functions.escape_format(
            escape_dn_str,
            'uid={0},cn={1}',
            uid,
            zone,
        )
    else:
        first_dn_part = ldap0.functions.escape_format(
            escape_dn_str,
            'uid={0}',
            uid,
        )
    return ','.join((first_dn_part, aeroot_dn))


def aedir_aehost_dn(
        fqdn: str,
        srvgrp: Optional[str] = None,
        zone: Optional[str] = None,
        aeroot_dn: str = AEDIR_SEARCH_BASE,
    ) -> str:
    """
    Returns a bind DN of a aeHost entry
    """
    if zone and srvgrp:
        first_dn_part = ldap0.functions.escape_str(
            escape_dn_str,
            'host=%s,cn=%s,cn=%s',
            fqdn,
            srvgrp,
            zone
        )
    else:
        first_dn_part = ldap0.functions.escape_str(
            escape_dn_str,
            'host=%s',
            fqdn
        )
    return ','.join((first_dn_part, aeroot_dn))


def aedir_aegroup_dn(
        aegroup_cn: str,
        aeroot_dn: str = AEDIR_SEARCH_BASE,
    ):
    """
    Returns a bind DN of a aeHost entry
    """
    zone_cn, _ = aegroup_cn.split('-', 1)
    return 'cn={0},cn={1},{2}'.format(
        escape_dn_str(aegroup_cn),
        escape_dn_str(zone_cn),
        aeroot_dn,
    )


class AEDirUrl(LDAPUrl):
    """
    LDAPUrl class for AE-DIR with some more LDAP URL extensions
    """

    def __init__(
            self,
            ldapUrl=None,
            urlscheme='ldap',
            hostport='',
            dn='',
            attrs=None,
            scope=None,
            filterstr=None,
            extensions=None,
            who=None,
            cred=None,
            trace_level=None,
            sasl_mech=None,
            pwd_filename=None,
        ):
        LDAPUrl.__init__(
            self,
            ldapUrl=ldapUrl,
            urlscheme=urlscheme,
            hostport=hostport,
            dn=dn,
            attrs=attrs,
            scope=scope,
            filterstr=filterstr,
            extensions=extensions,
            who=who,
            cred=cred,
        )
        self.trace_level = trace_level
        self.sasl_mech = sasl_mech
        self.pwd_filename = pwd_filename


def ldap_conf_url(ldap_url_class=AEDirUrl):
    """
    returns LDAPUrl object for uri and base read from ldap.conf
    """
    opt_uri = (
        ldap0.functions.get_option(ldap0.OPT_URI) or b''
    ).decode('utf-8').split(' ')[0].strip() or None
    ldap_url = ldap_url_class(ldapUrl=opt_uri)
    ldap_url.dn = (
        ldap0.functions.get_option(ldap0.OPT_DEFBASE) or b''
    ).decode('utf-8').strip() or None
    return ldap_url


class AEDirObject(ReconnectLDAPObject):
    """
    AE-DIR connection class
    """
    aeroot_filter: str = '(objectClass=aeRoot)'

    def __init__(
            self,
            ldap_url: str,
            trace_level: int = 0,
            retry_max: int = LDAP_MAXRETRYCOUNT,
            retry_delay: Union[int, float] = LDAP_RETRYDELAY,
            timeout: Union[int, float] = LDAP_TIMEOUT,
            who: Optional[str] = None,
            cred: Optional[bytes] = None,
            cacert_filename: Optional[str] = None,
            client_cert_filename: Optional[str] = None,
            client_key_filename: Optional[str] = None,
            cache_ttl: Union[int, float] = 0.0,
            sasl_authz_id: str = '',
        ):
        """
        Opens connection, sets some LDAP options and binds according
        to what's provided in `uri'.

        Extensions to parameters passed to ReconnectLDAPObject():
        `ldap_url'
          Can contain the full LDAP URL with authc information and base-DN
        `who'
          Bind-DN to be used (overrules ldap_url)
        `cred'
          Bind password to be used (overrules ldap_url)
        """
        # Parse/store LDAP URL into AEDirUrl instance
        if isinstance(ldap_url, str):
            self.ldap_url_obj = AEDirUrl(ldap_url)
        elif isinstance(ldap_url, AEDirUrl):
            self.ldap_url_obj = ldap_url
        elif ldap_url is None:
            self.ldap_url_obj = ldap_conf_url(ldap_url_class=AEDirUrl)
        else:
            raise ValueError('Invalid value for ldap_url: %r' % ldap_url)
        ReconnectLDAPObject.__init__(
            self,
            self.ldap_url_obj.connect_uri(),
            trace_level=trace_level or int(self.ldap_url_obj.trace_level or '0'),
            cache_ttl=cache_ttl,
            retry_max=retry_max,
            retry_delay=retry_delay,
        )
        # Set TLS options
        if self.ldap_url_obj.urlscheme != 'ldapi':
            self.set_tls_options(
                cacert_filename=cacert_filename,
                client_cert_filename=client_cert_filename,
                client_key_filename=client_key_filename,
            )
        # Set timeout values
        self.set_option(ldap0.OPT_NETWORK_TIMEOUT, timeout)
        self.set_option(ldap0.OPT_TIMEOUT, timeout)
        # Send StartTLS extended operation if clear-text connection was initialized
        if self.ldap_url_obj.urlscheme == 'ldap':
            self.start_tls_s()
        # Bind with authc information found in ldap_url and key-word arguments
        if (
                (
                    self.ldap_url_obj.urlscheme == 'ldapi'
                    and who is None
                )
                or
                (
                    self.ldap_url_obj.sasl_mech
                    and self.ldap_url_obj.sasl_mech.upper() == 'EXTERNAL'
                )
            ):
            sasl_authz_id = sasl_authz_id or self.ldap_url_obj.sasl_authzid or ''
            self.sasl_non_interactive_bind_s('EXTERNAL', authz_id=sasl_authz_id)
        else:
            if who is None:
                who = self.ldap_url_obj.who
            if cred is None:
                cred = self.ldap_url_obj.cred
            if who is not None:
                self.simple_bind_s(
                    who,
                    cred or '',
                    req_ctrls=[AuthorizationIdentityRequestControl()],
                )
        # determine the AE-DIR search base (aeRoot) and cache it
        self._search_base = (self.ldap_url_obj.dn or '').strip() or None
        self._search_base_dnobj = None
        # end of AEDirObject.__init__()

    @property
    def search_base(self):
        """
        Returns the aeRoot entry as byte-string
        """
        if self._search_base is not None:
            return self._search_base
        # read namingContexts from rootDSE
        self._search_base = self.read_rootdse_s(attrlist=['aeRoot']).entry_s['aeRoot'][0]
        self._search_base_dnobj = None
        return self._search_base

    @property
    def search_base_dnobj(self):
        """
        Returns the search base as DNObj instance.
        """
        if self._search_base_dnobj is not None:
            return self._search_base_dnobj
        self._search_base_dnobj = DNObj.from_str(self.search_base)
        return self._search_base_dnobj

    def find_byname(
            self, name: str,
            name_attr: str = 'cn',
            object_class: str = 'aeObject',
            attrlist: Optional[AttrList] = None,
        ) -> LDAPResult:
        """
        Returns a unique aeObject entry
        """
        return self.find_unique_entry(
            self.search_base,
            filterstr=escape_format(
                escape_filter_str,
                '(&(objectClass={oc})({at}={name}))',
                oc=object_class,
                at=name_attr,
                name=name,
            ),
            attrlist=attrlist,
        )

    def find_uid(
            self,
            uid: str,
            attrlist: Optional[AttrList] = None,
        ) -> LDAPResult:
        """
        Returns a unique aeUser or aeService entry found by uid
        """
        return self.find_unique_entry(
            self.search_base,
            filterstr='(uid={uid})'.format(
                uid=escape_filter_str(uid),
            ),
            attrlist=attrlist,
        )

    def find_aegroup(
            self,
            common_name: str,
            attrlist: AttrList = AEGroup.__must__,
        ) -> LDAPResult:
        """
        Returns a unique aeGroup entry
        """
        return AEGroup.from_search_result(
            self.find_byname(
                common_name,
                name_attr='cn',
                object_class='aeGroup',
                attrlist=attrlist,
            )
        )

    def find_aesrvgroup(
            self,
            common_name: str,
            attrlist: AttrList = AESrvGroup.__must__,
        ) -> LDAPResult:
        """
        Returns a unique aeGroup entry
        """
        return AESrvGroup.from_search_result(
            self.find_byname(
                common_name,
                name_attr='cn',
                object_class='aeSrvGroup',
                attrlist=attrlist,
            )
        )

    def find_aehost(
            self,
            host_name: str,
            attrlist: AttrList = AEHost.__must__,
        ) -> LDAPResult:
        """
        Returns a unique aeHost entry found by attribute 'host'
        """
        return AEHost.from_search_result(
            self.find_byname(
                host_name,
                name_attr='host',
                object_class='aeHost',
                attrlist=attrlist,
            )
        )

    def get_zoneadmins(
            self,
            ae_object_dn: str,
            attrlist: Optional[AttrList] = None,
            suppl_filter: str = '',
        ) -> List[LDAPResult]:
        """
        Returns LDAP search results of active aeUser entries of all
        zone-admins responsible for the given `ae_object_dn'.
        """
        ae_object_dnobj = DNObj.from_str(ae_object_dn)
        zone = self.read_s(
            str(ae_object_dnobj.slice(-len(self.search_base_dnobj)-1, None)),
            filterstr='(objectClass=aeZone)',
            attrlist=['aeZoneAdmins'],
        )
        if not (zone.entry_s and 'aeZoneAdmins' in zone.entry_s):
            return []
        return self.search_s(
            self.search_base,
            ldap0.SCOPE_SUBTREE,
            filterstr=(
                '(&'
                '(objectClass=aeUser)'
                '(aeStatus=0)'
                '(|{0})'
                '{1}'
                ')'
            ).format(
                compose_filter(
                    '|',
                    map_filter_parts(
                        'memberOf',
                        zone.entry_s.get('aeZoneAdmins', [])
                    ),
                ),
                suppl_filter,
            ),
            attrlist=attrlist,
        )
        # get_zoneadmins()

    def get_user_groups(self, uid: str, memberof_attr: str = 'memberOf') -> Set[str]:
        """
        Gets a set of DNs of aeGroup entries a AE-DIR user (aeUser or
        aeService) is member of
        """
        if memberof_attr:
            attrlist = [memberof_attr]
        else:
            attrlist = ['1.1']
        aeuser = self.find_uid(uid, attrlist=attrlist)
        if memberof_attr in aeuser.entry_s:
            memberof = aeuser.entry_s[memberof_attr]
        else:
            ldap_result = self.search_s(
                self.search_base,
                ldap0.SCOPE_SUBTREE,
                ldap0.functions.escape_format(
                    escape_filter_str,
                    '(&(objectClass=aeGroup)(member={user_dn}))',
                    user_dn=aeuser.dn_s,
                ),
                attrlist=['1.1'],
            )
            memberof = [res.dn_s for res in ldap_result]
        return set(memberof) # get_user_groups()

    def search_service_groups(
            self,
            service_dn: str,
            filterstr='',
            attrlist: Optional[AttrList] = None,
            req_ctrls: Optional[List[ldap0.controls.RequestControl]] = None,
        ):
        """
        starts searching all service group entries the aeHost/aeService defined by
        service_dn is member of
        """
        aeservice_entry = self.read_s(
            service_dn,
            attrlist=['aeSrvGroup']
        ).entry_s
        aesrvgroup_dn_list = [str(DNObj.from_str(service_dn).parent())]
        aesrvgroup_dn_list.extend(aeservice_entry.get('aeSrvGroup', []))
        srvgroup_filter = compose_filter('|', map_filter_parts('entryDN', aesrvgroup_dn_list))
        if filterstr:
            srvgroup_filter = '(&{0}{1})'.format(filterstr, srvgroup_filter)
        msg_id = self.search(
            self.search_base,
            ldap0.SCOPE_SUBTREE,
            srvgroup_filter,
            attrlist=attrlist or ['1.1'],
            req_ctrls=req_ctrls,
        )
        return msg_id

    def get_service_groups(
            self,
            service_dn: str,
            filterstr: str = '',
            attrlist: Optional[AttrList] = None,
            req_ctrls: Optional[List[ldap0.controls.RequestControl]] = None,
        ) -> Iterator[LDAPResult]:
        """
        returns all service group entries the aeHost/aeService defined by
        service_dn is member of
        """
        msg_id = self.search_service_groups(
            service_dn,
            filterstr=filterstr,
            attrlist=attrlist,
            req_ctrls=req_ctrls,
        )
        return self.results(msg_id)

    def get_user_srvgroup_relations(
            self,
            uid,
            aesrvgroup_dn,
            ref_attrs=None
        ):
        """
        Gets relationship between a aeUser and a aeSrvGroup object by
        simply returning the matching attributes of the aeSrvGroup entry
        """
        aeuser_memberof = self.get_user_groups(uid)
        ref_attrs = ref_attrs or AESRVGROUP_GROUPREF_ATTRS
        aesrvgroup = self.read_s(
            aesrvgroup_dn,
            filterstr='(objectClass=aeSrvGroup)',
            attrlist=ref_attrs
        )
        if not aesrvgroup.entry_s:
            raise ValueError('Empty search result for %r' % aesrvgroup_dn)
        srvgroup_relations = []
        for attr_type in ref_attrs:
            if attr_type in aesrvgroup.entry_s:
                for attr_value in aesrvgroup.entry_s[attr_type]:
                    if attr_value.lower() in aeuser_memberof:
                        srvgroup_relations.append(attr_type)
                        break
        return srvgroup_relations
        # end of get_user_srvgroup_relations()

    def get_user_service_relations(
            self,
            uid,
            service_dn,
            ref_attrs=None
        ):
        """
        get relation(s) between aeUser specified by uid with
        aeHost/aeService specified by service_dn

        returns set instance of relationship attribute names,
        which is a sub-set of AESRVGROUP_GROUPREF_ATTRS
        """
        aesrvgroups = self.get_service_groups(service_dn, attrlist=None)
        aesrvgroup_dn_set = set()
        for res in aesrvgroups:
            aesrvgroup_dn_set.update([aesrvgroup.dn_s for aesrvgroup in res.rdata])
        result = set()
        for aesrvgroup_dn in aesrvgroup_dn_set:
            result.update(
                self.get_user_srvgroup_relations(
                    uid,
                    aesrvgroup_dn=aesrvgroup_dn,
                    ref_attrs=ref_attrs,
                )
            )
        return result

    def search_users(
            self,
            service_dn: str,
            ae_status: int = 0,
            filterstr: str = '(|(objectClass=aeUser)(objectClass=aeService))',
            attrlist: Optional[AttrList] = None,
            ref_attr: str = 'aeLoginGroups',
            req_ctrls: Optional[List[ldap0.controls.RequestControl]] = None,
        ):
        """
        starts async search for all aeUser/aeService entries having the
        appropriate relationship on given aeHost/aeService
        """
        aesrvgroups = self.get_service_groups(
            service_dn,
            filterstr='({0}=*)'.format(ref_attr),
            attrlist=[ref_attr],
        )
        ref_attrs_groups = set()
        for res in aesrvgroups:
            for srvgroup in res.rdata:
                ref_attrs_groups.update([
                    av.lower()
                    for av in srvgroup.entry_s.get(ref_attr, [])
                ])
        if not ref_attrs_groups:
            return None
        user_group_filter = '(&(aeStatus={0}){1}{2})'.format(
            str(int(ae_status)),
            filterstr,
            compose_filter('|', map_filter_parts('memberOf', ref_attrs_groups))
        )
        msg_id = self.search(
            self.search_base,
            ldap0.SCOPE_SUBTREE,
            user_group_filter,
            attrlist=attrlist,
            req_ctrls=req_ctrls,
        )
        return msg_id

    def get_users(
            self,
            service_dn,
            ae_status=0,
            filterstr='(|(objectClass=aeUser)(objectClass=aeService))',
            attrlist: Optional[AttrList] = None,
            ref_attr='aeLoginGroups',
            req_ctrls: Optional[List[ldap0.controls.RequestControl]] = None,
        ):
        """
        returns all aeUser/aeService entries having the appropriate
        relationship on given aeHost/aeService  as list of 2-tuples
        """
        msg_id = self.search_users(
            service_dn,
            ae_status=ae_status,
            filterstr=filterstr,
            attrlist=attrlist,
            ref_attr=ref_attr,
            req_ctrls=req_ctrls,
        )
        if msg_id is None:
            return []
        return self.results(msg_id)

    def get_next_id(
            self,
            id_pool_dn: Optional[str] = None,
            id_pool_attr: str = 'gidNumber',
        ) -> int:
        """
        consumes next ID by sending MOD_INCREMENT modify operation with
        pre-read entry control
        """
        id_pool_dn = id_pool_dn or self.search_base
        prc = PreReadControl(criticality=True, attrList=[id_pool_attr])
        res = self.modify_s(
            id_pool_dn,
            [(ldap0.MOD_INCREMENT, id_pool_attr.encode('ascii'), [b'1'])],
            req_ctrls=[prc],
        )
        return int(res.ctrls[0].res.entry_s[id_pool_attr][0])

    def find_highest_id(
            self,
            id_pool_dn: Optional[str] = None,
            id_pool_attr: str = 'gidNumber'
        ) -> int:
        """
        search the highest value of `id_attr' by using server-side (reverse) sorting
        """
        id_pool_dn = id_pool_dn or self.search_base
        # reverse sorting request control
        sss_control = SSSRequestControl(
            criticality=True,
            ordering_rules=['-'+id_pool_attr]
        )
        # send search request
        msg_id = self.search(
            id_pool_dn,
            ldap0.SCOPE_SUBTREE,
            '(&(!(objectClass=aePosixIdRanges))({0}=*))'.format(id_pool_attr),
            attrlist=[id_pool_attr],
            sizelimit=1,
            req_ctrls=[sss_control],
        )
        # collect result
        ldap_result: List[LDAPResult] = []
        try:
            for res in self.results(msg_id):
                ldap_result.extend(res.rdata)
        except ldap0.SIZELIMIT_EXCEEDED:
            pass
        highest_id_number = int(ldap_result[0].entry_s[id_pool_attr][0])
        return highest_id_number

    def add_aeuser(
            self,
            zone: str,
            uid: str,
            ae_person_dn: str,
            ae_status: AEStatus = AEStatus.active,
            posix_id: Optional[int] = None,
            ae_ticket_id: Optional[str] = None,
            description: Optional[str] = None,
            login_shell: Optional[str] = None,
            home_directory: str = '/home/{uid}',
            pwd_policy_subentry: str = 'cn=ppolicy-users,cn=ae,ou=ae-dir',
        ):
        """
        add a new aeUser entry beneath given zone
        """
        # read associated aePerson entry
        try:
            ae_person = self.read_s(
                ae_person_dn,
                filterstr='(aeStatus=0)',
                attrlist=('mail', 'sn', 'givenName'),
            )
        except ldap0.NO_SUCH_OBJECT:
            raise ldap0.NO_SUCH_OBJECT('Could not read aePerson entry %r' % (ae_person_dn,))
        if posix_id is None:
            # get new POSIX-UID/GID
            posix_id = self.get_next_id()
        # DN of new entry
        add_dn = aedir_aeuser_dn(uid, zone=zone, aeroot_dn=self.search_base)
        # generate modlist (entry's content)
        ae_user = AEUser(
            aeStatus=ae_status,
            uid=uid,
            aePerson=ae_person.dn_o,
            uidNumber=posix_id,
            gidNumber=posix_id,
            givenName=ae_person.entry_s['givenName'][0],
            sn=ae_person.entry_s['sn'][0],
            mail=ae_person.entry_s['mail'][0],
            cn='{givenName} {sn}'.format(
                givenName=ae_person.entry_s['givenName'][0],
                sn=ae_person.entry_s['sn'][0],
            ),
            homeDirectory=home_directory.format(uid=uid),
            displayName='{givenName} {sn} ({uid}/{uidNumber})'.format(
                givenName=ae_person.entry_s['givenName'][0],
                sn=ae_person.entry_s['sn'][0],
                uid=uid,
                uidNumber=posix_id,
            ),
            pwdPolicySubentry=DNObj.from_str(pwd_policy_subentry),
            aeTicketId=ae_ticket_id,
            description=description,
            loginShell=login_shell,
        )
        add_res = self.add_s(
            add_dn,
            ae_user.ldap_entry(),
            req_ctrls=[PostReadControl(
                criticality=True,
                attrList=['*', '+']
            )],
        )
        return add_res.ctrls[0].res.entry_s

    def get_role_groups(
            self,
            service_dn: str,
            role_attrs
        ) -> Dict[str, Set[str]]:
        """
        Return user groups for role permissions on a certain service.
        """
        srv_grps = self.get_service_groups(service_dn, attrlist=role_attrs)
        role_groups: Dict[str, Set[str]] = {}
        for role_attr in role_attrs:
            role_groups[role_attr] = set()
            for res in srv_grps:
                for srv_grp in res.rdata:
                    role_groups[role_attr].update(srv_grp.entry_s.get(role_attr, []))
        return role_groups

    def get_role_groups_filter(
            self,
            service_dn: str,
            assertion_type: str,
            role_attr: str = 'aeVisibleGroups',
        ) -> str:
        """
        Return filter string for searching user groups with given permissions.
        """
        groups = self.get_role_groups(service_dn, [role_attr])[role_attr]
        if groups:
            entry_dn_filter = ldap0.filter.compose_filter(
                '|',
                ldap0.filter.map_filter_parts(assertion_type, groups),
            )
        else:
            entry_dn_filter = ''
        return entry_dn_filter

    def get_sudoers(
            self,
            service_dn: str,
            attrlist: Optional[AttrList] = None,
            req_ctrls: Optional[List[ldap0.controls.RequestControl]] = None,
        ):
        """
        Return sudoers entries for a host/service.
        """
        attrlist = attrlist or AE_SUDOERS_ATTRS
        req_ctrls = req_ctrls or []
        req_ctrls.append(DereferenceControl(True, {'aeVisibleSudoers': attrlist}))
        msg_id = self.search_service_groups(service_dn, attrlist=['1.1'], req_ctrls=req_ctrls)
        sudoers: List[LDAPResult] = []
        for ldap_res in self.results(msg_id):
            for res in ldap_res.rdata:
                if res.ctrls and res.ctrls[0].controlType == DereferenceControl.controlType:
                    sudoers.extend(res.ctrls[0].derefRes['aeVisibleSudoers'])
        return sudoers

    def add_aehost(
            self,
            host_name: str,
            srvgroup_name: str,
            suppl_srvgroup_names: Optional[StrList] = None,
            ppolicy_name: str = 'ppolicy-systems',
            entry: Optional[EntryStr] = None,
            password: Optional[str] = None,
        ):
        """
        Add a new host entry for given `host_name' (FQDN) beneath aeSrvGroup
        defined by `srvgroup_name'
        """
        srvgroup = self.find_aesrvgroup(srvgroup_name)
        if srvgroup.aeStatus != AEStatus.active:
            raise ValueError(
                'Service group %r not active, aeStatus is %d' % (
                    srvgroup.dn_s,
                    srvgroup.aeStatus,
                )
            )
        ppolicy = self.find_byname(
            ppolicy_name,
            name_attr='cn',
            object_class='pwdPolicy',
            attrlist=['1.1'],
        )
        ae_host = AEHost(
            parent_dn=srvgroup.dn_s,
            aeStatus=AEStatus.active,
            cn=host_name,
            host=host_name,
            pwdPolicySubentry=ppolicy.dn_o,
        )
        host_entry = ae_host.ldap_entry()
        if entry:
            host_entry.update({
                at: [av.encode(self.encoding) for av in avs]
                for at, avs in entry.items()
            })
        self.add_s(ae_host.dn_s, host_entry)
        if password:
            self.passwd_s(ae_host.dn_s, None, password)
        # end of add_aehost()

    def set_password(
            self, name: str,
            password: Optional[bytes],
            filterstr_tmpl: str = AUTHC_ENTITY_FILTER_TMPL,
        ) -> Tuple[str, Optional[str]]:
        """
        Set a password of an entity specified by name.
        The entity can be a aeUser, aeService or aeHost and its full DN
        is searched by unique find based on filterstr_tmpl.

        A 2-tuple with DN of the entry and password is returned as result.

        The caller has to handle exception ldap0.err.NoUniqueEntry.
        """
        res = self.find_unique_entry(
            self.search_base,
            scope=ldap0.SCOPE_SUBTREE,
            filterstr=filterstr_tmpl.format(escape_filter_str(name)),
            attrlist=['pwdPolicySubentry'],
        )
        generated_password = None
        if password is None:
            pwd_policy = self.read_s(
                res.entry_s['pwdPolicySubentry'][0],
                filterstr='(objectClass=pwdPolicy)',
                attrlist=['pwdMinLength'],
            )
            pwd_min_length = int(pwd_policy.entry_s.get('pwdMinLength', ['0'])[0])
            password = generated_password = random_string(length=max(PWD_LENGTH, pwd_min_length))
        self.passwd_s(res.dn_s, None, password)
        return (res.dn_s, generated_password)
        # end of set_password()

    def add_aezone(self, zone_name: str, ticket_id: str, zone_desc: str = '') -> str:
        """
        Add a new zone entry with init tag and standard zone admin/auditors groups.
        Returns DN of zone as string.
        """
        ae_zone = AEZone(
            parent_dn=self.search_base_dnobj,
            aeStatus=AEStatus.active,
            cn=zone_name,
            aeTicketId=ticket_id,
            description=zone_desc,
        )
        ae_tag = AETag(
            parent_dn=ae_zone.dn_o,
            aeStatus=AEStatus.active,
            cn=zone_name + '-init',
            description="Initialization of zone '{0}'".format(zone_name)
        )
        ae_zone_admins = AEGroup(
            parent_dn=ae_zone.dn_o,
            aeStatus=AEStatus.active,
            cn=zone_name+'-zone-admins',
            aeTag=ae_tag.cn,
            aeTicketId=ticket_id,
            description="Group members are zone admins who can manage zone '{zone_cn}'".format(
                zone_cn=zone_name,
            ),
            gidNumber=self.get_next_id(
                id_pool_dn=self.search_base,
                id_pool_attr='gidNumber',
            )
        )
        ae_zone_auditors = AEGroup(
            parent_dn=ae_zone.dn_o,
            aeStatus=AEStatus.active,
            cn=zone_name+'-zone-auditors',
            aeTag=ae_tag.cn,
            aeTicketId=ticket_id,
            description="Group members are zone auditors who can read zone '{zone_cn}'".format(
                zone_cn=zone_name,
            ),
            gidNumber=self.get_next_id(
                id_pool_dn=self.search_base,
                id_pool_attr='gidNumber',
            )
        )
        # actually add the entries via LDAP
        for ae_obj in (ae_zone, ae_tag, ae_zone_admins, ae_zone_auditors):
            self.add_s(ae_obj.dn_s, ae_obj.ldap_entry())
        # add aeTag attribute to zone entry after adding all other entries
        self.modify_s(
            ae_zone.dn_s,
            [
                (ldap0.MOD_ADD, b'aeTag', [ae_tag.cn.encode('utf-8')]),
                (ldap0.MOD_ADD, b'aeZoneAdmins', [ae_zone_admins.dn_o.encode('utf-8')]),
                (ldap0.MOD_ADD, b'aeZoneAuditors', [ae_zone_auditors.dn_o.encode('utf-8')]),
            ]
        )
        return ae_zone.dn_s
        # end of add_aezone()


def members2uids(members: Sequence[str]) -> List[str]:
    """
    transforms list of group member DNs into list of uid values
    """
    return [
        dn[4:].split(',')[0]
        for dn in members
    ]


def init_logger(
        logger_qualname: str,
        logging_config: Optional[str] = AE_LOGGING_CONFIG,
    ):
    """
    Returns logger instance
    """
    if logging_config:
        logging.config.fileConfig(logging_config)
    logger = logging.getLogger(logger_qualname)
    return logger
