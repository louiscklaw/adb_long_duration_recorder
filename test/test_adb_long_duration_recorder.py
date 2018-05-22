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

from pprint import pprint

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

    def get_file_in_dir(self, dir_path='/home/logic', mask='*.mp4'):
        """get the path, list the file matching the path"""
        match_files=[]
        re_filemask = fnmatch.translate(mask)

        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                if re.match(re_filemask, filename):
                    match_files.append(os.path.join(dir_path, filename))
            # list the current directory only
            break

        return match_files


    def setUp(self):
        print('setup (topic) test')
        self.clear_the_stage()

    def tearDown(self):
        print('teardown (topic) test')
        self.clear_the_stage()

    def test_helloworld(self):
        AdbLongDurationRecorder('xxxxxx').helloworld()

    def test_create_instance(self, UDID=TestSetting.ANDROID_UDID, maximum_length=180):
        record_instance = AdbLongDurationRecorder(UDID, maximum_length=maximum_length)
        self.assertIsInstance(record_instance, AdbLongDurationRecorder, 'cannot create instance')
        return record_instance


    def test_get_filename_in_android(self, UDID=TestSetting.ANDROID_UDID):
        TEST_SET={
            1: ['/sdcard/temp_record_0.mp4'],
            3: ['/sdcard/temp_record_0.mp4', '/sdcard/temp_record_1.mp4', '/sdcard/temp_record_2.mp4']
        }
        record_instance=self.test_create_instance(UDID)
        for repeat_num, filenames in TEST_SET.items():
            result_filenames=record_instance._get_filename_in_android(repeat_num)
            self.assertEqual(result_filenames, filenames, 'fail')

    def tefalsest_get_start_command(self, UDID=TestSetting.ANDROID_UDID):

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

    def test_list_process(self):
        record_instance = self.test_create_instance()
        ps_list = record_instance.list_process()

        return ps_list

    def assert_check_process_by_pid(self, pid):
        process_list = self.test_list_process()

        self.assertGreater(process_list.find(str(pid)), -1, 'cannot find the target process from host {}'.format(process_list))


    def test_adb_start_record(self, duration=99, UDID=TestSetting.ANDROID_UDID, maximum_length=180):
        record_instance = self.test_create_instance(maximum_length=maximum_length)
        record_instance.adb_start_record(duration)

        self.assertGreater(int(record_instance.record_pid), 1)

        self.assert_check_process_by_pid(record_instance.record_pid)

        # print(record_instance.record_files_android_path)
        # self.assertEqual('',dir(record_instance),'fail')

        # self.assertIn('/sdcard/temp_record_0.mp4', record_instance.record_files_android_path, 'fail')

        # TODO: remov me
        # list_mp4_command=r'adb shell ls -l /sdcard/\*.mp4'
        # splitted_command = shlex.split(list_mp4_command)
        # result = subprocess.check_output(splitted_command)

        return record_instance

    def test_list_file_in_android(self):
        file_test_vector='test_vector.mp4'
        test_path = '/sdcard'
        file_on_android = os.path.join(test_path, file_test_vector)

        os.system('adb shell touch {}'.format(file_on_android))

        record_instance = self.test_create_instance()
        result = record_instance.list_file_in_android()

        self.assertIn(file_test_vector,result, 'fail listing file in android')



    def t1est_get_pull_command(self, UDID=TestSetting.ANDROID_UDID):
        mp4_file = '/sdcard/screenrecord_1.mp4'
        record_instance = self.test_adb_start_record()
        commands = record_instance._get_pull_command(mp4_file)
        self.assertEqual(commands, '/usr/bin/adb -s {} pull {} /tmp'.format(UDID, mp4_file), 'failed {}'.format(commands))

    def test_ls_files(self):
        test_file = '/tmp/test.mp4'
        test_dir = os.path.dirname(test_file)
        filemask = '*.mp4'

        os.system('touch {}'.format(test_file))
        file_in_tmp_dir = self.get_file_in_dir(test_dir,filemask)

        self.assertEqual(file_in_tmp_dir, [test_file], 'the target file not found')

    # def test_adb_pull_record(self, duration=180, mp4_epxected, maximum_duration=2):
    #     record_instance = self.test_adb_start_record(duration, maximum_duration=maximum_duration)

    #     time.sleep(duration)

    def test_get_start_record_command(self):
        TEST_SET={
            0: '/usr/bin/adb -s VZHGLMA742802935 shell screenrecord --time-limit 0 /sdcard/temp_record_0.mp4',
            1: '/usr/bin/adb -s VZHGLMA742802935 shell screenrecord --time-limit 1 /sdcard/temp_record_0.mp4',
            180: '/usr/bin/adb -s VZHGLMA742802935 shell screenrecord --time-limit 180 /sdcard/temp_record_0.mp4',
            181: '/usr/bin/adb -s VZHGLMA742802935 shell screenrecord --time-limit 181 /sdcard/temp_record_0.mp4',
        }
        for duration, expected_command in TEST_SET.items():
            record_instance = self.test_create_instance(maximum_length=duration)
            commands = record_instance._get_start_record_command()

            self.assertEqual(expected_command, commands, 'the generated command not match {}'.format(commands))

    def test_get_adb_command_head(self):
        record_instance = self.test_create_instance()
        result = record_instance._get_adb_command_head()

        self.assertEqual('/usr/bin/adb -s {}'.format(TestSetting.ANDROID_UDID), result, 'the generated command not match')

    def te1st_adb_pull_records(self):
        TEST_SET = {
            1: ['/tmp/temp_record_0.mp4' ],
            # 3: ['/tmp/temp_record_0.mp4', '/tmp/temp_record_1.mp4'],
        }
        UDID = TestSetting.ANDROID_UDID
        for record_test_duration, filenames in TEST_SET.items():
            # record_instance = self.test_adb_start_record(record_test_duration, maximum_length=2)

            record_instance = AdbLongDurationRecorder(UDID)
            record_instance.adb_start_record()

            time.sleep(record_test_duration+1)

            file_on_android = record_instance.list_file_in_android()
            pprint(file_on_android)
            assert False

            record_instance.adb_pull_records()



            mp4_files_found = self.get_file_in_dir('/tmp','*.mp4')
            self.assertEqual(filenames, mp4_files_found, 'cannot find mp4 files under directory')




        # self.fail(file_in_tmp_dir)

    # def test_adb_record_start_to_end(self):
    #     record_instance = self.test_create_instance()
    #     record_instance.adb_start_record(3)
    #     record_instance.adb_kill_record()

if __name__ == '__main__':
    unittest.main(verbosity=2)
