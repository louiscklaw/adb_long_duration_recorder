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

    @pytest.mark.wip
    def test_use(self, duration=1):
        DUT_UDID = TestSettings.udid
        test_instance = AdbLongDurationRecorder(DUT_UDID)

        test_instance.start_recording()
        time.sleep(duration)
        test_instance.stop_record()

        list_mp4_files = test_instance.send_command_get_response('ls -l /mnt/user/0/primary/*.mp4')
        self.assertGreater(list_mp4_files.find('screen_record_1.mp4'), 0)

        # test_instance.pull_record()
        # test_instance.rm_record()


if __name__ == '__main__':
    unittest.main(verbosity=2)
