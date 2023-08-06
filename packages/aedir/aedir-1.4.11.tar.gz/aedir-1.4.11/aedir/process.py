# -*- coding: ascii -*-
"""
aedir.process - base class for maintenance processes and tools etc.

See https://ae-dir.com/python.html for details.

(c) 2016-2021 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

# Imports from Python's standard lib
import socket
import sys
import os
import time
import configparser
import email.utils
from typing import Optional
from smtplib import SMTPRecipientsRefused

# Imports from ldap0 module package
import ldap0
import ldap0.functions

from . import init_logger, AE_LOGGING_CONFIG, AEDirObject

# exported symbols
__all__ = [
    'AEProcess',
    'TimestampStateMixin',
]

# Exception class used for catching all exceptions
CatchAllException = Exception

# set global trace level of ldap0 module package
ldap0._trace_level = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))


class AEProcess:
    """
    Base process class
    """
    script_version = '(no version)'
    logging_config = AE_LOGGING_CONFIG
    cfg_parser_class = configparser.ConfigParser
    cfg_default_section = configparser.DEFAULTSECT
    __slots__ = (
        '_cfg',
        'cfg_filename',
        'host_fqdn',
        'initial_state',
        'ldap0_trace_level',
        '_ldap_conn',
        'ldap_url',
        'logger',
        'run_counter',
        'script_name',
        'start_time',
    )

    def __init__(
            self,
            logger_name: Optional[str] = None,
        ):
        self.script_name = os.path.basename(sys.argv[0])
        self.host_fqdn = socket.getfqdn()
        self.logger = init_logger(
            logger_name or '{mod_name}.{class_name}'.format(
                mod_name=__spec__.name,
                class_name=self.__class__.__name__,
            ),
            self.logging_config,
        )
        self.logger.debug('Logger config: %s', self.logging_config)
        self.logger.debug('Logger name: %s', self.logger.name)
        if 'LOG_LEVEL' in os.environ:
            self.logger.setLevel(os.environ['LOG_LEVEL'].upper())
        self.logger.debug(
            'Starting %s %s on %s',
            sys.argv[0],
            self.script_version,
            self.host_fqdn
        )
        # no config yet
        self.cfg_filename = None
        self._cfg = None
        # not really started yet
        self.start_time = None
        self.run_counter = None
        self.initial_state = None
        # no LDAP connection yet
        self.ldap_url = None
        self._ldap_conn = None
        self.ldap0_trace_level = ldap0._trace_level

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._ldap_conn is not None:
            try:
                self.logger.debug(
                    'Close LDAP connection to %r',
                    self._ldap_conn.ldap_url_obj.connect_uri()
                )
                self._ldap_conn.unbind_s()
            except (ldap0.LDAPError, AttributeError):
                pass

    @property
    def cfg(self):
        """
        lazy parsing of config file
        """
        if self._cfg is not None:
            # already parsed the config before
            return self._cfg
        if self.cfg_filename is None:
            raise RuntimeError(
                'No config file defined with {0}.cfg_filename !'.format(self.__class__.__name__)
            )
        self.logger.debug('Reading config file %r', self.cfg_filename)
        cfg_parser = self.cfg_parser_class(
            interpolation=None,
            default_section=self.cfg_default_section,
        )
        with open(self.cfg_filename, 'r') as cfg_file:
            cfg_parser.read_file(cfg_file)
        self._cfg = cfg_parser.defaults()
        self.logger.debug('Configuration: %r', self._cfg)
        return self._cfg

    @property
    def ldap_conn(self):
        """
        return a LDAP connection to \xC6-DIR server
        """
        if self._ldap_conn is None:
            self.logger.debug('Connecting to %r...', self.ldap_url)
            self._ldap_conn = AEDirObject(self.ldap_url, trace_level=self.ldap0_trace_level)
            self.logger.debug(
                'Connected to %r bound as %r',
                self._ldap_conn.ldap_url_obj.connect_uri(),
                self._ldap_conn.whoami_s(),
            )
        return self._ldap_conn

    @ldap_conn.setter
    def ldap_conn(self, ldap_conn):
        """
        attach activated LDAP connection to this process instance
        """
        self._ldap_conn = ldap_conn

    def smtp_connection(
            self,
            url,
            local_hostname=None,
            ca_certs=None,
            debug_level=0,
        ):
        """
        Open SMTP connection if not yet done before
        """
        # lazy import of optional dependency
        import mailutil
        local_hostname = local_hostname or self.host_fqdn
        self.logger.debug('Opening SMTP connection to %r from %r ...', url, local_hostname)
        smtp_conn = mailutil.smtp_connection(
            url,
            local_hostname=local_hostname,
            ca_certs=ca_certs,
            debug_level=debug_level,
        )
        return smtp_conn

    def send_simple_message(
            self,
            smtp_conn,
            from_addr,
            to_addr,
            subject_tmpl: str,
            tmpl_filename: str,
            msg_attrs: dict,
            raise_refused: bool = False,
        ):
        """
        Send single message for a user,
        generate message body and subject based on templates and msg_attrs
        """
        self.logger.debug('msg_attrs = %r', msg_attrs)
        smtp_subject = subject_tmpl.format(**msg_attrs)
        self.logger.debug('smtp_subject = %r', smtp_subject)
        with open(tmpl_filename, 'r', encoding='utf-8') as tfile:
            tmpl_txt = tfile.read()
        smtp_message = tmpl_txt.format(**msg_attrs)
        self.logger.debug('smtp_message = %r', smtp_message)
        try:
            smtp_conn.send_simple_message(
                from_addr,
                [to_addr],
                'utf-8',
                (
                    ('From', from_addr),
                    ('Date', email.utils.formatdate(time.time(), True)),
                    ('Subject', smtp_subject),
                    ('To', to_addr),
                ),
                smtp_message,
            )
        except SMTPRecipientsRefused as smtp_error:
            self.logger.error(
                'Recipient %r rejected: %s',
                to_addr,
                smtp_error
            )
            if raise_refused:
                raise smtp_error
        else:
            self.logger.info('Sent message (%d chars) to %r', len(smtp_message), to_addr)
        # end of send_simple_message()

    def get_state(self):
        """
        get current state (to be overloaded by derived classes)
        """
        return self.initial_state

    def set_state(self, state):
        """
        set current state (to be overloaded by derived classes)
        """

    def run_worker(self, state):
        """
        one iteration of worker run (to be overloaded by derived classes)

        must return next state to be passed to set_state()
        """
        # this should never be called anyway => log warning
        self.logger.warning(
            'Nothing done in %s.run_worker() with state %r',
            self.__class__.__name__,
            state,
        )


    def exit(self):
        """
        method called on exit
        (to be overloaded by derived classes, e.g. for logging a summary)
        """
        self.logger.debug('Exiting %s', self.__class__.__name__)

    def run(self, max_runs=1, run_sleep=60.0):
        """
        the main program
        """
        self.start_time = time.time()
        self.run_counter = 0
        try:
            # first run
            self.set_state(self.run_worker(self.get_state()))
            self.run_counter += 1
            while self.run_counter < max_runs or max_runs is None:
                # further runs
                self.set_state(self.run_worker(self.get_state()))
                self.run_counter += 1
                time.sleep(run_sleep)
        except KeyboardInterrupt:
            self.logger.info('Exit on keyboard interrupt')
            self.exit()
        except CatchAllException as err:
            self.logger.error(
                'Unhandled exception %s.%s: %s',
                err.__class__.__module__,
                err.__class__.__name__,
                err,
                exc_info=__debug__
            )
        else:
            self.exit()
        # end of AEProcess.run()


class TimestampStateMixin:
    """
    Mix-in class for AEProcess which implements timestamp-based
    state strings in a file
    """
    initial_state = '19700101000000Z'

    def get_state(self):
        """
        Read the timestamp of last run from file `sync_state_filename'
        """
        try:
            with open(self.state_filename, 'rb') as file_obj:
                last_run_timestr = file_obj.read().strip().decode('utf-8') or self.initial_state
            # check syntax by parsing the string
            ldap0.functions.strp_secs(last_run_timestr)
        except (IOError, ValueError) as err:
            self.logger.warning(
                'Error reading timestamp from file %r: %r',
                self.state_filename,
                err
            )
            # reset to initial state as recovery from error
            last_run_timestr = self.initial_state
        else:
            self.logger.debug(
                'Read last run timestamp %r from file %r',
                last_run_timestr,
                self.state_filename,
            )
        return last_run_timestr
        # end of get_state()

    def set_state(self, current_time_str):
        """
        Write the current state
        """
        if not current_time_str:
            current_time_str = self.initial_state
        try:
            # Write the last run timestamp
            with open(self.state_filename, 'wb') as file_obj:
                file_obj.write(current_time_str.encode('utf-8'))
        except IOError as err:
            self.logger.warning('Could not write %r: %r', self.state_filename, err)
        else:
            self.logger.debug('Wrote %r to %r', current_time_str, self.state_filename)
        # end of set_state()
