# -*- coding: ascii -*-
"""
Automatic tests for simple functions in module aedir.process

See https://ae-dir.com/python.html for details.
"""

# from Python's standard lib
import asyncore
import os
import smtpd
import email.parser
import time
import threading
import unittest

import ldap0.functions

# import module to be tested herein
import aedir
import aedir.process
from aedir.test import AETest


class FakeSMTPServer(smtpd.SMTPServer):
    smtp_listen_address = ('127.0.0.1', 52525)

    def __init__(self):
        smtpd.SMTPServer.__init__(
            self,
            self.smtp_listen_address,
            None,
            data_size_limit=30000,
            decode_data=False,
        )
        self.messages_received = 0

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        message = email.parser.Parser().parsestr(data.decode('utf-8'))
        self.messages_received += 1



class TestProcess(aedir.process.AEProcess):
    """
    base class for test processes, not directly used
    """
    logging_config = os.path.join(os.getcwd(), 'tests', 'ae-logging.conf')
    cfg_default_section = 'test'


class TestKeyboardInterruptProcess(TestProcess):
    """
    test dummy class which raises KeyboardInterrupt
    """

    def run_worker(self, state):
        raise KeyboardInterrupt


class TestTimestampStateProcess(aedir.process.TimestampStateMixin, TestProcess):
    """
    test dummy class which writes timestamp file
    """

    def run_worker(self, state):
        aedir.process.AEProcess.run_worker(self, state)
        # send a test e-mail
        smtp_conn = self.smtp_connection(
            'smtp://%s:%d' % FakeSMTPServer.smtp_listen_address,
            debug_level=0
        )
        self.send_simple_message(
            smtp_conn,
            'ae-dir-test-from@example.com',
            'ae-dir-test-to@example.com',
            'Test mail to user {username}',
            'tests/test_message.txt',
            dict(
                username='test',
                firstname='Theo',
                lastname='Tester',
            ),
        )
        # simply return current time as current state
        return ldap0.functions.strf_secs(None)


class TestAedirProcess(AETest):
    """
    test class for aedir.process
    """

    @classmethod
    def setUpClass(cls):
        super(TestAedirProcess, cls).setUpClass()
        cls.server = list(cls.servers.values())[0]
        cls.smtp_server = FakeSMTPServer()
        cls.async_loop_thread = threading.Thread(target=asyncore.loop,kwargs = {'timeout':1})
        cls.async_loop_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.smtp_server.close()
        cls.async_loop_thread.join()

    def test001_process(self):
        TestTimestampStateProcess.state_filename = os.path.join(self.server.testrundir, 'aeprocess.state')
        with TestTimestampStateProcess() as ae_process:
            ae_process.ldap_url = self.server.ldapi_uri
            self.assertEqual(ae_process.ldap_conn.whoami_s(), 'dn:cn=root,'+self.ae_suffix)
            ae_process.run(max_runs=1, run_sleep=0.01)
            self.assertEqual(ae_process.run_counter, 1)
            self.assertEqual(self.smtp_server.messages_received, 1)
            valid_timestamps = set([ldap0.functions.strf_secs(None)])
            ae_process.run(max_runs=3, run_sleep=0.01)
            self.assertEqual(ae_process.run_counter, 3)
            self.assertEqual(self.smtp_server.messages_received, 4)
            valid_timestamps.add(ldap0.functions.strf_secs(None))
            with open(ae_process.state_filename, 'rb') as file_obj:
                last_state = file_obj.read().strip().decode('utf-8')
            self.assertIn(
                last_state,
                valid_timestamps,
                'Wrong timestamp %r read from %r, expected one of %r' % (
                    last_state,
                    ae_process.state_filename,
                    valid_timestamps,
                ),
            )

    def test002_keyboard_interrupt(self):
        with TestKeyboardInterruptProcess() as ae_process:
            ae_process.run(max_runs=1)

    def test003_error_handling_on_exit(self):
        with TestTimestampStateProcess() as ae_process:
            ae_process.ldap_url = self.server.ldapi_uri
            self.assertEqual(ae_process.ldap_conn.whoami_s(), 'dn:cn=root,'+self.ae_suffix)
            # provoke an unbind exception in AEProcess.__exit__() by already unbinding here
            ae_process.ldap_conn.unbind_s()

    def test004_cfg(self):
        with TestTimestampStateProcess() as ae_process:
            ae_process.cfg_filename = None
            with self.assertRaises(RuntimeError):
                ae_process.cfg
            ae_process.cfg_filename = 'tests/ae-dir-process-test.cfg'
            self.assertEqual(len(ae_process.cfg), 2)
            self.assertEqual(ae_process.cfg['foo'], 'bar')
            self.assertEqual(ae_process.cfg['bar'], 'foo')
            with self.assertRaises(KeyError):
                ae_process.cfg['not-existent']

    def test005_ldap_conn_setter(self):
        with TestTimestampStateProcess() as ae_process:
            ae_process.ldap_url = self.server.ldapi_uri
            old_ldap_conn = ae_process.ldap_conn
            # reset AEProcess._ldap_conn to "not connected"
            ae_process._ldap_conn = None
            new_ldap_conn = ae_process.ldap_conn
            self.assertNotEqual(id(old_ldap_conn), id(new_ldap_conn))
            self.assertEqual(old_ldap_conn.whoami_s(), new_ldap_conn.whoami_s())
            self.assertEqual(ae_process.ldap_conn.whoami_s(), 'dn:cn=root,'+self.ae_suffix)
            ae_process.ldap_conn = old_ldap_conn
            self.assertEqual(id(old_ldap_conn), id(ae_process.ldap_conn))


if __name__ == '__main__':
    unittest.main()
