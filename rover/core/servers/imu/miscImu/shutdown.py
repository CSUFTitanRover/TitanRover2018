#!/usr/bin/python
from time import sleep
import RPi.GPIO as GPIO
from subprocess import call, Popen
from deepstream import post
import subprocess, re

GPIO.setmode(GPIO.BCM)
buttonPin = 5

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    pressed = not GPIO.input(buttonPin)
    if pressed:
        p = Popen(["screen", "-ls"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        rmatch = re.findall(r"\d{1,}\.\w+", out)
        for item in rmatch:
            call(["screen", "-S", item, "-X", "kill"])
        sleep(3)
        try:
            post({}, 'imu')
        except:
            print("Deepstream Not available")
        call(["shutdown", "now"])
    sleep(.1)
