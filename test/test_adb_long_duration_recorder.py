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
import unittest
import pytest
import time
import subprocess
import shlex

import threading

from src.adb_long_duration_recorder import *


class TestSettings():
    udid = 'VZHGLMA750201895'


def setUpModule():
    print('setup (topic) module')


def tearDownModule():
    print('teardown (topic) module')


class TestAdbLongDurationRecorder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setup (topic) class')

    @classmethod
    def tearDownClass(cls):
        print('teardown (topic) class')

    def setUp(self):
        print('setup (topic) test')
        os.system('adb shell rm -rf /mnt/uiser/0/primary/*.mp4')
        os.system('adb kill-server')

        os.system('rm -rf /tmp/*.mp4')

    def tearDown(self):
        print('teardown (topic) test')

    def test_helloworld(self, udid=TestSettings.udid):
        test_instance = AdbLongDurationRecorder(udid)

        test_instance.close_device()

    def test_get_record_commands_single(self):
        DUT_UDID = TestSettings.udid
        TEST_SET = {
            1: 'screenrecord --time-limit 1 /sdcard/screen_{UDID}_0.mp4'.format(UDID=DUT_UDID),
            2: 'screenrecord --time-limit 1 /sdcard/screen_{UDID}_0.mp4 & screenrecord --time-limit 1 /sdcard/screen_{UDID}_1.mp4'.format(UDID=DUT_UDID),
            3: 'screenrecord --time-limit 1 /sdcard/screen_{UDID}_0.mp4 & screenrecord --time-limit 1 /sdcard/screen_{UDID}_1.mp4 & screenrecord --time-limit 1 /sdcard/screen_{UDID}_2.mp4'.format(UDID=DUT_UDID),
        }
        for num_of_repeat, expected_commands in TEST_SET.items():
            test_instance = AdbLongDurationRecorder(DUT_UDID)
            test_command = test_instance._get_record_commands(1, num_of_repeat)
            self.assertEqual(expected_commands, test_command, 'the generated command is not correct {}'.format(test_command))

    def list_android_file(self, expected_file):
        return self.test_instance.send_command_get_response('ls -l {}'.format(expected_file))

    def check_android_file_exist(self, file_to_check):
        list_expected_file = self.list_android_file(file_to_check)
        self.assertGreater(0, list_expected_file.find('No such file or directory'), list_expected_file)

    def check_pc_file_exist(self, file_to_check):
        ls_command = 'ls -l {}'.format(file_to_check)
        result = subprocess.check_output(shlex.split(ls_command))
        self.assertGreater(0, result.find('No such file or directory'), result)

    def test_capture(self, duration=1, duration_per_session=180):
        DUT_UDID = TestSettings.udid

        target_file = 'screen_VZHGLMA750201895_0.mp4'
        android_temp_dir = '/mnt/user/0/primary/'
        pc_temp_dir = '/tmp'
        android_mp4_fullpath = os.path.join(android_temp_dir, target_file)
        pc_mp4_fullpath = os.path.join(pc_temp_dir, target_file)

        self.test_instance = AdbLongDurationRecorder(DUT_UDID)

        self.test_instance.start_recording(duration, duration_per_session)
        time.sleep(duration + 1)
        self.test_instance.stop_record()
        self.check_android_file_exist(android_mp4_fullpath)

        self.test_instance.pull_record()
        self.check_pc_file_exist(pc_mp4_fullpath)

        # assert False
        self.test_instance.rm_record()

    def test_rm_record(self):
        DUT_UDID = TestSettings.udid
        self.test_instance = AdbLongDurationRecorder(DUT_UDID)
        self.test_instance.rm_record()

    def test_get_rm_command(self):
        DUT_UDID = TestSettings.udid
        self.test_instance = AdbLongDurationRecorder(DUT_UDID)
        # assert False
        result = self.test_instance._get_rm_commands()
        self.assertEqual('rm -rf /sdcard/screen_*_*.mp4', result)

    def test_captures(self):
        DUT_UDID = TestSettings.udid
        duration = 10
        duration_per_session = 5
        total_file_num = duration / duration_per_session

        target_files = ['screen_VZHGLMA750201895_{}.mp4'.format(filenum) for filenum in range(0, total_file_num)]
        android_temp_dir = '/mnt/user/0/primary'
        pc_temp_dir = '/tmp'

        android_files = ['{}/{}'.format(android_temp_dir, target_file) for target_file in target_files]
        pc_files = ['{}/{}'.format(pc_temp_dir, target_file) for target_file in target_files]

        # android_mp4_fullpath = os.path.join(android_temp_dir, target_file)
        # pc_mp4_fullpath = os.path.join(pc_temp_dir, target_file)

        self.test_instance = AdbLongDurationRecorder(DUT_UDID)

        self.test_instance.start_recording(duration, duration_per_session)
        time.sleep(duration + 1)
        self.test_instance.stop_record()

        for android_file in android_files:
            self.check_android_file_exist(android_file)

        self.test_instance.pull_record()
        # self.check_pc_file_exist(pc_mp4_fullpath)

        assert False
        self.test_instance.rm_record()

    def thread_sleep(self, seconds_to_sleep):
        print('sleep i {}'.format(seconds_to_sleep))

        self.test_instance_1.try_sleep(seconds_to_sleep)

        print('sleep i {} done'.format(seconds_to_sleep))

    @pytest.mark.wip
    def test_double_connect(self):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        ts = []
        for i in range(5, 0, -1):
            t = threading.Thread(target=self.thread_sleep, args=(i,))
            ts.append(t)

        [t.start() for t in ts]
        [t.join() for t in ts]

        assert False


if __name__ == '__main__':
    unittest.main(verbosity=2)
