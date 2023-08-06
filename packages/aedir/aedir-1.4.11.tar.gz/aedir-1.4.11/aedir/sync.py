# -*- coding: ascii -*-
"""
aedir.sync - sub-module for implementing simple sync processes

See https://ae-dir.com/python.html for details.

(c) 2016-2021 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

from collections import defaultdict
from typing import Dict, Optional, Union

import ldap0
import ldap0.filter
from ldap0 import LDAPError
from ldap0.typehints import AttrList, EntryMixed, RequestControls

import aedir.process


class AEInputConnector(aedir.process.AEProcess):
    """
    Base class for sync processes writing data into \xC6-DIR
    """

    def _search_entries(
            self,
            base: Optional[str] = None,
            scope: int = ldap0.SCOPE_SUBTREE,
            filterstr: str = '(objectClass=*)',
            attrlist: Optional[AttrList] = None,
            req_ctrls: Optional[RequestControls] = None,
            timeout: Union[int, float] = -1,
        ) -> Dict[str, EntryMixed]:
        """
        read existing \xC6-DIR entries return
        """
        if base is None:
            base = self.ldap_conn.search_base
        self.logger.debug('Searching old entries with %r', filterstr)
        msg_id = self.ldap_conn.search(
            base,
            scope,
            filterstr=filterstr,
            attrlist=attrlist,
            req_ctrls=req_ctrls,
            timeout=timeout,
        )
        res = {}
        for ldap_res in self.ldap_conn.results(msg_id):
            for rdata in ldap_res.rdata:
                res[rdata.dn_s] = rdata.entry_as
        self.logger.debug('Found %d aePerson entries', len(res))
        return res

    def _iterate_source(self):
        """
        iterate over source data
        """

    def _apply_changes(self, source_iter, old_entries):
        """
        apply necessary changes to target entries
        """
        ldap_write_error_count = 0
        aeperson_change_count = defaultdict(lambda: 0)
        for new_dn, new_entry in source_iter:
            try:
                ldap_op = self.ldap_conn.ensure_entry(
                    new_dn,
                    new_entry.ldap_entry(),
                    old_entry=old_entries.get(new_dn, None),
                )
            except LDAPError as err:
                self.logger.error('Error writing %r: %s', new_dn, err)
                ldap_write_error_count += 1
            else:
                if ldap_op:
                    self.logger.info('Write operations on %r: %r', new_dn, ldap_op)
                    for ldap_op in ldap_op or []:
                        aeperson_change_count[ldap_op.rtype] += 1
        if aeperson_change_count:
            self.logger.info(
                'Changes applied to aePerson entries: add=%d modify=%d',
                aeperson_change_count[ldap0.RES_ADD],
                aeperson_change_count[ldap0.RES_MODIFY],
            )
        else:
            self.logger.debug('No changes applied to aePerson entries')
        if ldap_write_error_count:
            self.logger.warning('%d write operations failed!', ldap_write_error_count)
        # end of _apply_changes()

    def run_worker(self, state):
        """
        mainly for demonstration purpose
        """
        self._apply_changes(
            # for better performance later we first read all existing entries
            self._search_entries(),
            self._iterate_source(),
        )
