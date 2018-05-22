#!/usr/bin/env python
# coding:utf-8

#! /usr/env python3
# -*- coding: utf-8 -*-

"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

Todo:
    * For module TODOs

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""


import os
import sys
import logging
import traceback
import subprocess
import shlex
import math
import logging

from pprint import pprint


def get_host_command_output(command):

    result = subprocess.check_output(shlex.split(command)).decode('utf-8')
    return result.strip()

class StatusText:
    status_start='start'
    status_end='end'

class ErrorText:
    error_1='error 1'
    ERROR_PULLING_SCREEN_RECORD='error during pulling screen record'
    ERROR_GETTING_PULL_SCREEN_RECORD_COMMAND='error getting pull screen record command'
    ERROR_SENDING_SUBPROCESS_COMMAND='error sending command using popen'
    ERROR_LISTING_PROCESS='error during list the process on host'
    ERROR_KILLING_RECORDING='error duruing killing the recording process'

class RunEnv:
    ADB_BIN_PATH=get_host_command_output('which adb')
    FASTBOOT_BIN_PATH = get_host_command_output('which fastboot')



class ErrorException(Exception):
    pass


class AdbLongDurationRecorder:
    temp_record_filenames = ['temp_record_{}.mp4'.format(i) for i in range(0, 999)]

    class StatusText:
        status_1='status1'

    class ExitNum:
        normal_exit=0
        error_exit=-1

    def __init__(self, udid, android_store_dir='/sdcard', local_store_dir='/tmp', maximum_length=180):
        self.udid = udid
        self.android_store_dir = android_store_dir
        self.local_store_dir = local_store_dir
        self.maximum_length = maximum_length

    def _send_host_command(self, command, emitt_exception=False, use_shell=False):
        """accept string command, split it and feed to the subpeocess.check_output"""
        try:
            splitted_command = shlex.split(command)
            result = subprocess.check_output(splitted_command, shell=use_shell)
            result = result.decode('utf-8')
            return result

        except Exception as e:
            ErrorText.ERROR_SENDING_SUBPROCESS_COMMAND
            if emitt_exception:
                raise e

    def _get_record_filenames(self, repeat_times=1):
        return self.temp_record_filenames[0:repeat_times]


    def _get_adb_command_head(self):
        udid = self.udid

        adb_bin_path = RunEnv.ADB_BIN_PATH

        return '{} -s {}'.format(adb_bin_path, udid)

    def _get_filename_in_android(self, repeat_times=1):
        android_store_dir = self.android_store_dir
        record_filenames = self._get_record_filenames(repeat_times)

        record_files_android_path = ['{}/{}'.format(android_store_dir, record_filename) for record_filename in record_filenames]
        return record_files_android_path

    def _get_start_record_command(self, repeat_times=1 ):
        # adb shell screenrecord /sdcard/example.mp4
        adb_command_head = self._get_adb_command_head()
        udid = self.udid
        time_limit = self.maximum_length

        record_files_android_path = self._get_filename_in_android(repeat_times)

        # adb shell screenrecord --time-limit <TIME>
        commands = ' & '.join(['{} shell screenrecord --time-limit {} {}'.format(adb_command_head, time_limit,record_file) for record_file in record_files_android_path])

        self.record_files_android_path = record_files_android_path


        return commands

    def _get_rm_record_command(self):
        adb_command_head = self._get_adb_command_head()
        android_store_dir = self.android_store_dir

        command = '{} rm {}'.format(adb_command_head, android_store_dir)

        return command

    def _get_record_pid_command(self):
        udid = self.udid
        command = 'ps -xa | grep -i adb | grep -v grep | grep -i screenrecord | grep {}'.format(udid)

        return command

    def _get_kill_record_command(self, pid):
        command = 'kill {}'.format(pid)
        return command

    def _get_pull_command(self, file_on_android):
        adb_command_head = self._get_adb_command_head()
        local_store_dir = self.local_store_dir

        pull_command = '{} pull {} {}'.format(adb_command_head, file_on_android, local_store_dir)

        return pull_command

    def _lock_resource(self):
        pass

    def _release_resource(self):
        pass

    def get_recording_pid(self):
        command = shlex.split(self._get_record_pid_command())
        result = subprocess.check_output(command).decode('utf-8').strip()
        pid=result.split()[0]
        return pid

    def _count_repeat(self, duration, max_number_output =999):

        repeat = max_number_output
        if duration != -1:
            int(math.ceil(duration / self.maximum_length))
        return repeat

    def list_process(self):
        try:
            command_list_process = 'ps -ef'
            result = self._send_host_command(command_list_process, use_shell=True)
            return result
        except Exception as e:
            logging.error(ErrorText.ERROR_LISTING_PROCESS)
            raise e


    def list_file_in_android(self, to_list_dir='/sdcard', mask='*.mp4'):
        target_file_mask = '/sdcard'
        list_android_command = 'adb shell ls %s' % target_file_mask
        splitted_command = shlex.split(list_android_command)
        files = subprocess.check_output(splitted_command).decode('utf-8')

        return files

    def _start_background_process(self, command):
        try:
            splitted_command = shlex.split(command)
            p = subprocess.Popen(splitted_command)
            return p.pid
        except Exception as e:
            raise e


    def adb_start_record(self, duration=-1):
        """to start the recording
        Args:
            duration: the duration of recording , -1 for very long
        """
        try:
            time_limit=self.maximum_length

            repeat = self._count_repeat(duration)
            command = self._get_start_record_command(repeat)

            record_pid = self._start_background_process(command)
            self.record_pid = record_pid

            logging.info('test start done')

        except Exception as e:
            raise e

        return self

    def adb_kill_record(self):
        """to kill the recording"""
        logging.debug('kill recording')

        try:
            pid = self.pid
            kill_command = shlex.split(self._get_kill_record_command(pid))
            self._send_host_command(kill_command)

        except Exception as e:
            logging.error(ErrorText.ERROR_KILLING_RECORDING)
            raise e

    def adb_pull_record(self, record_file_to_pull):
        try:
            command = self._get_pull_command(record_file_to_pull)
            self._send_host_command(command)
        except Exception as e:
            raise e
        return self

    def adb_pull_records(self):
        local_store_dir = self.local_store_dir
        record_files_android_paths = self.record_files_android_path

        self.actual_record_pulled=[]
        try:
            for record_files_android_path in record_files_android_paths:
                self.adb_pull_record(record_files_android_path)
                self.actual_record_pulled.append(record_files_android_path)

        except Exception as e:
            logging.error(ErrorText.ERROR_PULLING_SCREEN_RECORD)
            raise e

        return self

    def adb_rm_record(self):
        android_store_dir = self.android_store_dir
        command = self._get_rm_record_command()
        result = self._send_host_command(command)

        return self

    def combine_record(self):
        # ffmpeg -i "concat:input1.mp4|input2.mp4|input3.mp4" -c copy output.mp4
        pass

    def helloworld(self):
        print('helloworld')


if __name__ == '__main__':
    main()
