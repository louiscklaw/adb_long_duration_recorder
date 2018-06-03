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

from src.device import *

from src.adb_long_duration_recorder import *


class TestSettings():
    udid = get_devices()[0]


class ffmpeg_utilities():
    def helloworld():
        print('ffmpeg_helloworld')


class TestAdbLongDurationRecorder(unittest.TestCase):
    def setUp(self):
        # print('setup (topic) test')
        # os.system('adb shell rm -rf /mnt/user/0/primary/*.mp4')
        # os.system('adb kill-server')

        # os.system('rm -rf /tmp/*.mp4')
        os.system('adb shell  input keyevent 224 224 224')
        os.system('adb shell rm -f /data/system/locksettings.db* ')
        os.system('adb shell svc power stayon true')
        os.system('adb shell rm -rf /sdcard/*.mp4')

    def tearDown(self):
        pass

    # def test_helloworld(self, udid=TestSettings.udid):
    #     test_instance = AdbLongDurationRecorder(udid)
    #     test_instance.close_device()

    def test_get_command(self):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        commands = self.test_instance_1._get_record_command('bitrate', 'duration_s', 'file_name')
        self.assertEqual('screenrecord --bit-rate bitrate --time-limit duration_s file_name', commands, 'get_command is wrong')

    def test_use_sample(self):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        self.test_instance_1.start_recording(20, 3)
        time.sleep(10)

        self.test_instance_1.stop_record()
        self.test_instance_1.pull_record()
        # self.test_instance_1.combine_files()
