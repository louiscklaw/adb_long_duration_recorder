#!/usr/bin/python

import os.path as op

from adb import adb_commands
from adb import sign_m2crypto

import time

# KitKat+ devices require authentication
signer = sign_m2crypto.M2CryptoSigner(op.expanduser('~/.android/adbkey'))
# Connect to the device
device = adb_commands.AdbCommands()
device.ConnectDevice(rsa_keys=[signer])

def screencapture():
    print(device.Shell('screencap -p /sdcard/screen.png'))
    print(device.Shell('ls -l /sdcard'))
    screencapture = device.Pull('/sdcard/screen.png')
    f = open('/tmp/screencapture.png','wb')
    f.write(screencapture)
    f.close()

def screenrecord(duration=10):

    try:
        print(device.Shell('screenrecord  --time-limit {} /sdcard/screen.mp4'.format(duration)))

    except Exception as e:
        pass
    time.sleep(3)

    # print(device.Shell('ls -l /sdcard'))
    screencapture = device.Pull('/sdcard/screen.mp4')
    f = open('/home/logic/screencapture.mp4','wb')
    f.write(screencapture)
    f.close()


screenrecord()
