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

from src.adb_long_duration_recorder import *


import unittest



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

class Test_topic(unittest.TestCase):

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

    def test_helloworld(self):

        AdbLongDurationRecorder('xxxxxx').helloworld()




if __name__ == '__main__':
    unittest.main(verbosity=2)
