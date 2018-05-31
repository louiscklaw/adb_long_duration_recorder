#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint
import subprocess


def main():
    print('helloworld')
    p = subprocess.Popen('/usr/bin/adb shell "echo \$\$"')
    stdout = p.communicate()[0]
    print(stdout)


if __name__ == '__main__':
    main()
