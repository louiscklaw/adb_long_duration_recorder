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
from pprint import pprint


class ErrorException(Exception):
    pass


class AdbLongDurationRecorder:
    class StatusText:
        status_1='status1'

    class ExitNum:
        normal_exit=0
        error_exit=-1

    def __init__(self,udid):
        self.udid = udid
        pass

    def _get_start_record_command(self):
        # adb shell screenrecord /sdcard/example.mp4
        pass

    def _get_rm_record_command(self):
        pass

    def _get_kill_record_command(self):
        pass

    def _send_adb_command(self):
        pass

    def _lock_resource(self):
        pass

    def _release_resource(self):
        pass

    def adb_start_record(self, duration):
        """to start the recording
        Args:
            duration: the duration of recording , -1 for very long
        """
        pass

    def adb_kill_record(self):
        pass

    def adb_rm_record(self):
        pass

    def adb_pull_record(self):
        pass

    def combine_record(self):
        pass

    def helloworld(self):
        print('helloworld')


if __name__ == '__main__':
    main()
