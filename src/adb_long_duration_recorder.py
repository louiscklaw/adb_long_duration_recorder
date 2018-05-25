#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

from adb import adb_commands
from adb import sign_m2crypto

RECORD_COMMAND_TEMPLATE =  'screenrecord --time-limit {} /sdcard/screen{}.mp4'

class AdbLongDurationRecorder:

    class ExitNum:
        EXIT_NORMAL=0
        EXIT_ERROR=-1

    class StatusText:
        status_start = 'start'
        status_end = 'end'

    class ErrorTexts:
        ERROR_CANNOT_CONNECT_TO_ANDROID='cannot connect to android'

    class CannotConnectToAndroid(Exception):
        def __init__(self, udid):
            logging.error(ErrorTexts.ERROR_CANNOT_CONNECT_TO_ANDROID)

            self.device = self.init_device()

    def _get_record_commands(self, record_duration=180, number_of_repeat=1):
        record_commands= [RECORD_COMMAND_TEMPLATE.format(record_duration, file_num) for file_num in range(0,number_of_repeat)]
        return ' & '.join(record_commands)

    def __init__(self, udid):
        self.android_udid = udid

    def helloworld(self):
        print('helloworld')

    def init_device(self, adbkey_path='~/.android/adbkey'):
        try:
            # KitKat+ devices require authentication
            signer = sign_m2crypto.M2CryptoSigner(op.expanduser(adbkey_path))
            # Connect to the device
            device = adb_commands.AdbCommands()
            device.ConnectDevice(rsa_keys=[signer], serial=self.android_udid)

            return device
        except Exception as e:
            raise self.CannotConnectToAndroid(self.android_udid)

    def start_recording(self, record_duration=180):
        logging.debug('start recording')
        self.record_commands = self._get_record_commands(record_duration=record_duration)

        from pprint import pprint
        pprint(self.record_commands)

    def stop_record(self):
        logging.debug('stop recording')

    def pull_record(self):
        logging.debug('pull record')

    def rm_record(self):
        logging.debug('rm_record')

def main():
    print('helloworld')


if __name__ == '__main__':
    main()
