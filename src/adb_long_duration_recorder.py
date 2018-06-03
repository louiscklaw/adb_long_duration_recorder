#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
import threading
import time
import subprocess
import shlex

from pprint import pprint

from device import *

import os.path as op


class AdbLongDurationRecorder:
    SCREEN_RECORD_FILENAME_TEMPLATE = '{}_screenrecord_{}.mp4'

    class ExitNum:
        EXIT_NORMAL = 0
        EXIT_ERROR = -1

    class StatusText:
        status_start = 'start'
        status_end = 'end'

    class ErrorTexts:
        ERROR_CANNOT_CONNECT_TO_ANDROID = 'cannot connect to android'
        ERROR_STOP_RECORDING = 'cannot stop recordings'
        ERROR_PULL_RECORDING = 'cannot pull recordings'
        ERROR_REMOVE_RECORDING = 'cannot remove recordings'
        ERROR_CLOSE_DEVICE = 'cannot close device'

    class CannotConnectToAndroid(Exception):
        def __init__(self, udid):
            logging.error(AdbLongDurationRecorder.ErrorTexts.ERROR_CANNOT_CONNECT_TO_ANDROID)

    def __init__(self, udid, tmp_dir = '/tmp'):
        self.android_udid = udid
        self.total_record_count = 0
        self.DEFAULT_RECORD_BITRATE = 2000000
        self.android_record_filepaths = []
        self.stop_thread_recording = False
        self.tmp_dir = tmp_dir

    def _get_mp4_filename(self, number_of_repeat=0):
        return [self.SCREEN_RECORD_FILENAME_TEMPLATE.format(self.android_udid, index) for index in range(0, number_of_repeat + 1)]

    def _get_record_string(self, duration=1, android_tmp_dir='/sdcard', num_of_repeat=5):
        record_files = [os.path.join(android_tmp_dir, 'screenrecor{}.mp4'.format(file_num)) for file_num in
                        range(0, num_of_repeat)]
        return ['screenrecord --time-limit {} {}'.format(duration, file_name) for file_name in record_files]

    def _get_record_command(self, bitrate, duration_s, file_name):
        return 'screenrecord --bit-rate {} --time-limit {} {}'.format(bitrate, duration_s, file_name)

    def _create_mp4_combine_text_file(self, files_to_combine, txt_file_path='/tmp/concat.txt'):
        file_content = '\n'.join(["file '{}'".format(filepath) for filepath in files_to_combine])
        with open(txt_file_path, 'w') as f:
            f.write(file_content)

    def try_thread_recording(self, UDID, record_repeat=999, length_per_recording=180):
        ANDROID_TMP_DIR = '/sdcard'

        record_filenames = ['{}_screenrecord_{}.mp4'.format(self.android_udid, file_no) for file_no in range(0, record_repeat + 1)]
        record_fullpaths = [os.path.join(ANDROID_TMP_DIR, record_filename) for record_filename in record_filenames]

        for android_record_fullpath in record_fullpaths:
            if not self.stop_thread_recording:
                self.total_record_count += 1
                self.android_record_filepaths.append(android_record_fullpath)

                p = get_device(UDID).shell(
                    [self._get_record_command(self.DEFAULT_RECORD_BITRATE, length_per_recording, android_record_fullpath)]
                )

                print('the record section done for {}'.format(android_record_fullpath))

    def stop_record(self):
        print('stop record called')
        UDID = self.android_udid
        self.stop_thread_recording = True
        get_device(UDID).shell(['killall -2 screenrecord'])
        time.sleep(1)

    def start_recording(self, duration_s=999, split_s=180):
        UDID = self.android_udid

        t = threading.Thread(target=self.try_thread_recording, args=(UDID, duration_s, split_s, ))
        t.start()

        self.record_thread = t

    def pull_all_record(self, save_to_dir='/tmp'):
        UDID = self.android_udid
        android_record_files = self.android_record_filepaths
        pc_record_files = ['{}/{}'.format(save_to_dir,os.path.basename(android_record_file)) for android_record_file in android_record_files]

        for android_record_file, pc_record_file in zip(android_record_files, pc_record_files):
            get_device(UDID).pull(android_record_file, pc_record_file)

        logging.debug('pulling done')

    def combine_files(self, files_to_combine, save_to_mp4_file):
        """to combine the mp4 files
        command: ffmpeg -f concat -i concat.txt -c copy  test.mp4
        """
        TMP_CONCAT_FILENAME = '{}_concat.txt'.format(self.android_udid)
        TMP_CONCAT_FILEPATH = os.path.join(self.tmp_dir, TMP_CONCAT_FILENAME)

        CONCAT_COMMAND = 'ffmpeg -y -f concat -i {} -c copy {}'.format(TMP_CONCAT_FILEPATH, save_to_mp4_file)
        splitted_command = shlex.split(CONCAT_COMMAND)

        self._create_mp4_combine_text_file(files_to_combine, TMP_CONCAT_FILEPATH)

        return subprocess.check_output(splitted_command)

