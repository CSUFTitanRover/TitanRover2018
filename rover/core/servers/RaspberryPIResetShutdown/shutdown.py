#!/usr/bin/python
from time import sleep
import RPi.GPIO as GPIO
from subprocess import call, Popen
from deepstream import post
import subprocess, re

GPIO.setmode(GPIO.BCM)
buttonPin = 5

'''
    This python script needs to be launched as root,
    also, any screen session that needs to be launched,
    needs to be launched as root.  This shutdown script
    will kill all the screen sessions, first, and then
    tell deepstream that there are no objects available
    on the assiciated records.  This is important for our 
    homebase to know that no records are available during 
    a shutdown, or also a restart.  This script will be 
    setup for restart capability also. Though on the i3 computer,
    we will lack GPIO pins, so we can modify some of the logic in this
    script as either a socket call to shutdown, a serial shutdown/restart,
    or some other method to reset operations.
'''

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    pressed = not GPIO.input(buttonPin)
    if pressed:
        p = Popen(["screen", "-ls"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        rmatch = re.findall(r"\d{1,}\.\w+", out)
        for item in rmatch:
            call(["screen", "-S", item, "-X", "kill"])
        #sleep(3)
        #post({}, 'imu')
        call(["shutdown", "now"])
    sleep(.1)
