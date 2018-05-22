#!/usr/bin/env python
# init_py_dont_write_bytecode

"""

Helloworld boilder plate

Naming style guideline
    https://google.github.io/styleguide/pyguide.html

unittest documentation
    https://docs.python.org/3/library/unittest.html

"""

import os
import sys
import time
import re

import logging
import fnmatch
import unittest

from src.adb_long_duration_recorder import *

class StatusText(object):
    """StatusText"""
    TEST_TOPIC1 = 'test topic1'
    SAMPLE_STATUS1 = '${sample status}1'
    SAMPLE_STATUS2 = '${sample status}2'
    SAMPLE_STATUS3 = '${sample status}3'

class ErrorText(object):
    """ErrorText"""
    TEST_TOPIC1 = 'test topic1'
    ERROR_STATUS1 = '${error text}1'
    ERROR_STATUS2 = '${error text}2'
    ERROR_STATUS3 = '${error text}3'

class TestSetting:
    """to store the test settings"""
    ANDROID_UDID = 'VZHGLMA742802935'

def setUpModule():
    print('setup (topic) module')
def tearDownModule():
    print('teardown (topic) module')

class Test_topic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setup (topic) class')

    @classmethod
    def tearDownClass(cls):
        print('teardown (topic) class')

    def clear_the_stage(self):
        self.clear_tmp_dir()

    def clear_tmp_dir(self):
        os.system('rm -rf /tmp/*.mp4')

    def clear_adb_process(self):
        os.system('killall adb')

    def get_file_in_dir(self, dir_path='/home/logic', mask='mp4'):
        """get the path, list the file matching the path"""
        re_filemask = fnmatch.translate(mask)

        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                print(filename)
                # if re.match(re_filemask, filename) else 0
            assert False


    def setUp(self):
        print('setup (topic) test')
        self.clear_the_stage()

    def tearDown(self):
        print('teardown (topic) test')
        self.clear_the_stage()

    def test_helloworld(self):
        AdbLongDurationRecorder('xxxxxx').helloworld()

    def test_create_instance(self, UDID=TestSetting.ANDROID_UDID):
        record_instance=AdbLongDurationRecorder(UDID)
        self.assertIsInstance(record_instance, AdbLongDurationRecorder, 'cannot create instance')
        return record_instance


    def test_get_start_command(self, UDID=TestSetting.ANDROID_UDID):

        TEST_SET={
            1: '/usr/bin/adb -s {UDID} shell screenrecord /sdcard/temp_record_0.mp4'.format(UDID=UDID),
            3: '/usr/bin/adb -s {UDID} shell screenrecord /sdcard/temp_record_0.mp4 & /usr/bin/adb -s {UDID} shell screenrecord /sdcard/temp_record_1.mp4 & /usr/bin/adb -s {UDID} shell screenrecord /sdcard/temp_record_2.mp4'.format(UDID=UDID),
        }

        record_instance=self.test_create_instance(UDID)
        for number, answer in TEST_SET.items():
            command = record_instance._get_start_record_command(number)
            self.assertEqual(command, answer, 'cannot get the start command 123{}'.format(command))

    def test_get_record_pid_command(self, UDID=TestSetting.ANDROID_UDID):
        record_instance=self.test_create_instance(UDID)
        result = record_instance._get_record_pid_command()
        self.assertEqual(result, 'ps -xa | grep -i adb | grep -v grep | grep -i screenrecord | grep {}'.format(UDID), 'the pid is not correct "{}"'.format(result))

    def test_get_kill_record_command(self,  UDID=TestSetting.ANDROID_UDID):
        TEST_SET=['999','10']

        record_instance=self.test_create_instance(UDID)
        for pid in TEST_SET:
            command = record_instance._get_kill_record_command(pid)
            self.assertEqual(command, 'kill {}'.format(pid), 'cannot get the kill command')


    def test_adb_command_head(self, UDID=TestSetting.ANDROID_UDID):
        record_instance = self.test_create_instance()
        adb_command_head = record_instance._get_adb_command_head()
        self.assertEqual(adb_command_head, '/usr/bin/adb -s {}'.format(UDID), 'failed {}'.format(adb_command_head))

    def test_adb_start_record(self, duration=-1, UDID=TestSetting.ANDROID_UDID):
        record_instance = self.test_create_instance()
        record_instance.adb_start_record(duration)
        return record_instance


    def test_get_pull_command(self, UDID=TestSetting.ANDROID_UDID):
        mp4_file = '/sdcard/screenrecord_1.mp4'
        record_instance = self.test_adb_start_record()
        commands = record_instance._get_pull_command(mp4_file)
        self.assertEqual(commands, '/usr/bin/adb -s {} pull {} /tmp'.format(UDID, mp4_file), 'failed {}'.format(commands))

    def test_ls_files(self):
        file_in_tmp_dir = self.get_file_in_dir('/home/logic/*.log')
        # self.fail(file_in_tmp_dir)



    def tes1t_adb_pull_records(self):
        record_test_duration=3
        record_instance = self.test_adb_start_record(record_test_duration)
        time.sleep(record_test_duration)
        record_instance.adb_pull_records()


        # self.fail(file_in_tmp_dir)

    # def test_adb_record_start_to_end(self):
    #     record_instance = self.test_create_instance()
    #     record_instance.adb_start_record(3)
    #     record_instance.adb_kill_record()

if __name__ == '__main__':
    unittest.main(verbosity=2)
