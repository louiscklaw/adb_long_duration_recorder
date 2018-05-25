#!/usr/bin/env python
# init_py_dont_write_bytecode

"""

Helloworld boilder plate

Naming style guideline
    https://google.github.io/styleguide/pyguide.html

unittest documentation
    https://docs.python.org/3/library/unittest.html

"""

import unittest
import pytest
import time

from src.adb_long_duration_recorder import *

class TestSettings():
    udid = 'VZHGLMA750201895'

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

    def tearDown(self):
        print('teardown (topic) test')


    def test_helloworld(self, udid=TestSettings.udid):
        test_instance = AdbLongDurationRecorder(udid)
        test_instance.helloworld()

        return test_instance

    @pytest.mark.wip
    def test_get_record_commands_single(self):
        TEST_SET={
            1: 'screenrecord --time-limit 1 /sdcard/screen0.mp4',
            2: 'screenrecord --time-limit 1 /sdcard/screen0.mp4 & screenrecord --time-limit 1 /sdcard/screen1.mp4',
            3: 'screenrecord --time-limit 1 /sdcard/screen0.mp4 & screenrecord --time-limit 1 /sdcard/screen1.mp4 & screenrecord --time-limit 1 /sdcard/screen2.mp4',
        }
        for num_of_repeat, expected_commands in TEST_SET.items():
            test_instance = self.test_helloworld()
            test_command = test_instance._get_record_commands(1,num_of_repeat)
            self.assertEqual(expected_commands, test_command, 'the generated command is not correct {}'.format(test_command))

    def test_use(self, duration=1):
        test_instance = self.test_helloworld()
        test_instance.start_recording()
        time.sleep(duration)
        test_instance.stop_record()
        test_instance.pull_record()
        test_instance.rm_record()


if __name__ == '__main__':
    unittest.main(verbosity=2)
