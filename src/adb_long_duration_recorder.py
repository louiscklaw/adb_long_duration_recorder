#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
import threading
import time

from pprint import pprint


from adb import adb_commands
from adb import sign_m2crypto

import os.path as op


class AdbLongDurationRecorder:
    SCREEN_RECORD_FILENAME_TEMPLATE = 'screen_{}_{}.mp4'

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

    def _get_record_filenames(self, number_of_repeat):
        SCREEN_RECORD_FILENAME_TEMPLATE = AdbLongDurationRecorder.SCREEN_RECORD_FILENAME_TEMPLATE
        udid = self.android_udid
        return [SCREEN_RECORD_FILENAME_TEMPLATE.format(udid, filenum) for filenum in range(0, number_of_repeat)]

    def _get_record_file_fullpaths(self, number_of_repeat=1):
        android_udid = self.android_udid
        android_tmp_path = self.android_tmp_path
        pc_tmp_path = self.pc_tmp_path

        filenames = self._get_record_filenames(number_of_repeat)

        android_file_fullpaths = [os.path.join(android_tmp_path, filename) for filename in filenames]
        pc_file_fullpaths = [os.path.join(pc_tmp_path, filename) for filename in filenames]

        return pc_file_fullpaths, android_file_fullpaths

    def _get_record_commands(self, record_duration=180, number_of_repeat=1):
        RECORD_COMMAND_TEMPLATE = 'screenrecord --time-limit {} {}'

        _, android_file_fullpaths = self._get_record_file_fullpaths(number_of_repeat)

        record_commands = [RECORD_COMMAND_TEMPLATE.format(record_duration, file_fullpath) for file_fullpath in android_file_fullpaths]

        return ' & '.join(record_commands)

    def _get_kill_command(self):
        kill_command = 'killall screenrecord'
        return kill_command

    def _get_rm_commands(self):
        filemask = AdbLongDurationRecorder.SCREEN_RECORD_FILENAME_TEMPLATE.replace('{}', '*')
        file_location = '/'.join([self.android_tmp_path, filemask])
        rm_command = 'rm -rf {}'.format(file_location)
        return rm_command

    def __init__(self, udid, max_filenum=99, android_tmp_path='/sdcard', pc_tmp_path='/tmp'):
        self.android_udid = udid
        self.android_tmp_path = android_tmp_path
        self.pc_tmp_path = pc_tmp_path
        self.record_fullpaths = self._get_record_file_fullpaths(max_filenum)

        self.device = self.device_connect()

        self.device_mutex = threading.Lock()

        # # NOTE: initialize the tmp directory on android
        # self.rm_record()
        # record_command = self._get_record_commands(record_duration=1)

    def __del__(self):
        self.close_device()

    def close_device(self):
        try:
            self.device.Close()
        except Exception as e:
            logging.error(self.ErrorTexts.ERROR_CLOSE_DEVICE)

    def helloworld(self):
        print('helloworld')

    def device_connect(self, adbkey_path='~/.android/adbkey'):
        try:
            # KitKat+ devices require authentication
            signer = sign_m2crypto.M2CryptoSigner(op.expanduser(adbkey_path))
            # Connect to the device
            device = adb_commands.AdbCommands()
            device.ConnectDevice(rsa_keys=[signer], serial=self.android_udid)

            return device

        except Exception as e:
            logging.error('cannot connect to android')
            raise e

    def open_device_send_command(self, command, command_timeout=180):
        try:
            self.device_mutex.acquire()
            device = self.device_connect()

            # result = device.Shell(command, timeout_ms=command_timeout)
            result = device.Shell(command)
            device.Close()

            time.sleep(0.1)

            self.device_mutex.release()

            return result

        except Exception as e:
            logging.error('error sending command {}'.format(command))
            raise e

    def thread_record(self, wanted_duration, max_record_duration=180):
        self.record_idx = 0
        record_duration = 0
        command_timeout = 180 * 1000

        _, android_file_fullpaths = self.record_fullpaths

        while record_duration < wanted_duration:
            duration_diff = wanted_duration - record_duration
            duration = min(max_record_duration, duration_diff)
            record_duration = record_duration + duration

            record_commands = 'screenrecord --time-limit {} {}'.format(duration, android_file_fullpaths[self.record_idx])

            # print(record_commands)
            self.open_device_send_command(record_commands, command_timeout)
            self.record_idx += 1

    def start_recording(self, record_duration=180, max_record_duration=180):
        logging.debug('start recording ')
        # record_commands = self._get_record_commands(record_duration=record_duration)
        # print(record_commands)
        t = threading.Thread(target=self.thread_record, args=(record_duration, max_record_duration,))
        t.start()

    def stop_record(self):
        logging.debug('stop recording')
        try:
            kill_command = self._get_kill_command()
            # self.device.Shell(kill_command)
            self.open_device_send_command(kill_command)

        except Exception as e:
            logging.error(AdbLongDurationRecorder.ErrorTexts.ERROR_STOP_RECORDING)
            raise e

    def write_binary_file(self, binary_stream, filepath):
        f = open(filepath, 'wb')
        f.write(binary_stream)
        f.close()

    def pull_single_record(self, android_file, pc_file):
        COMMAND_TIMEOUT = 3 * 1000
        try:
            device = self.device_connect()
            screencapture = device.Pull(android_file)
            self.write_binary_file(screencapture, pc_file)
            device.Close()

        except Exception as e:
            logging.error('error pulling file {}'.format(android_file))

            raise e

    def pull_record(self, path_to_save='/tmp'):
        logging.debug('pull record')
        try:
            pc_file_fullpaths, android_file_fullpaths = self.record_fullpaths

            print(self.record_idx)

            for i in range(0, self.record_idx + 1):
                android_file_fullpath = android_file_fullpaths[i]
                pc_file_fullpath = pc_file_fullpaths[i]

                self.pull_single_record(android_file_fullpath, pc_file_fullpath)
                #
                print(pc_file_fullpath)

        except Exception as e:
            logging.error(AdbLongDurationRecorder.ErrorTexts.ERROR_PULL_RECORDING)
            raise e

    def rm_record(self):
        logging.debug('rm_record')
        try:
            rm_command = self._get_rm_commands()
            self.open_device_send_command(rm_command)

        except Exception as e:
            logging.error(self.ErrorTexts.ERROR_REMOVE_RECORDING)
            print(rm_command)
            raise e

    def get_hostname(self):
        return self.device.Shell('hostname')

    def try_sleep(self, seconds_s):
        SLEEP_COMMAND = 'sleep {}'.format(seconds_s)
        try:
            print(self.open_device_send_command(SLEEP_COMMAND))
        except Exception as e:
            raise e

    def send_command_get_response(self, command):
        device = self.device_connect()
        result = device.Shell(command)
        device.Close()
        return result


def main():
    print('helloworld')


if __name__ == '__main__':
    main()
