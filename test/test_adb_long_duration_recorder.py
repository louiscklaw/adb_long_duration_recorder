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

@unittest.skip('skip for quick test')
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

    def get_media_info(self, filepath):
        result = subprocess.check_output(shlex.split('ffprobe {}'.format(filepath))).decode('utf-8')
        return result

    def get_expected_durations(self, duration, range_s=2):
        # TODO: very ugly implementation of testing duration
        return ['Duration: 00:00:{}'.format(duration + i) for i in range(-range_s, range_s + 1)]

    def list_files(self, list_dir='/tmp'):
        return subprocess.check_output(shlex.split(r'ls -1 {}'.format(list_dir))).decode('utf-8').split()

    def test_get_command(self):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        commands = self.test_instance_1._get_record_command('bitrate', 'duration_s', 'file_name')
        self.assertEqual('screenrecord --bit-rate bitrate --time-limit duration_s file_name', commands,
                         'get_command is wrong')

    def inspect_file_duration(self, filepath, test_duration, expected_range=2):
        media_info_result = self.get_media_info(filepath)
        expected_durations = self.get_expected_durations(test_duration, expected_range)
        return any([media_info_result.find(expected_duration) for expected_duration in expected_durations])

    def inspect_number_of_file(self, android_serial, mp4_store_path, expected_number_of_file=1):
        tmp_mp4_on_host = self.list_files(mp4_store_path)
        expected_mp4_files = ['{}_screenrecord_{}.mp4'.format(android_serial, index) for index in
                              range(0, expected_number_of_file )]
        for expected_mp4 in expected_mp4_files:
            self.assertIn(expected_mp4, tmp_mp4_on_host)

    def test_get_mp4_filename(self):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        default_call_result = self.test_instance_1._get_mp4_filename()
        self.assertEqual(['{}_screenrecord_0.mp4'.format(DUT_UDID)], default_call_result,
                         'result of default call is wrong')

        for i in range(0, 3):
            call_result = self.test_instance_1._get_mp4_filename(i)
            self.assertEqual(['{}_screenrecord_{}.mp4'.format(DUT_UDID, idx) for idx in range(0, i + 1)], call_result,
                             'call_result is incorrect')


    def test_use_sample1(self, test_duration=6):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        self.test_instance_1.start_recording()
        time.sleep(test_duration)

        self.test_instance_1.stop_record()
        self.test_instance_1.pull_all_record()
        # self.test_instance_1.combine_files()

        self.assertTrue(self.inspect_file_duration('/tmp/{}_screenrecord_0.mp4'.format(DUT_UDID), test_duration),
                        'media duration is wrong')

    def test_use_sample2(self, test_duration_s=6):
        DUT_UDID = TestSettings.udid
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)

        self.test_instance_1.start_recording(split_s=3)
        time.sleep(test_duration_s)

        self.test_instance_1.stop_record()
        self.test_instance_1.pull_all_record()

        self.inspect_number_of_file(DUT_UDID, '/tmp', 2)
        self.assertTrue(all(
            [self.inspect_file_duration('/tmp/{}_screenrecord_{}.mp4'.format(DUT_UDID, idx), 3 )  for idx in range(0,2)]
        ))


class TestAdbLongDurationRecorder_PostProcess(unittest.TestCase):
    def test_helloworld(self):
        print('helloworld')

    def check_file_exist(self, filepath):
        COMMAND = 'ls -l {}'.format(filepath)
        split_command = shlex.split(COMMAND)
        result = subprocess.check_output(split_command)
        if result.find('No such') > -1:
            return False
        else:
            return True

    def test_create_mp4_combine_text_file(self):
        DUT_UDID = TestSettings.udid
        TMP_CONCAT_TXT = '/tmp/test_concat.txt'

        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)
        self.test_instance_1._create_mp4_combine_text_file(['file1.mp4', 'file2.mp4','file3.mp4'], TMP_CONCAT_TXT)

        self.assertTrue(self.check_file_exist(TMP_CONCAT_TXT), 'the {} file not exist'.format(TMP_CONCAT_TXT))

    def test_combine_video(self):
        COMBINED_MP4_FILE ='/tmp/combined.mp4'

        DUT_UDID = TestSettings.udid


        MP4_FILES = ['VZHGLMA750201895_screenrecord_0.mp4']*100
        self.test_instance_1 = AdbLongDurationRecorder(DUT_UDID)
        self.test_instance_1.combine_files(MP4_FILES, COMBINED_MP4_FILE)

        self.assertTrue(self.check_file_exist(COMBINED_MP4_FILE))