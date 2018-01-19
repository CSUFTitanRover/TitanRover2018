#!/bin/sh

### BEGIN INIT INFO
# Provides:             RoverMobilityServer
# Required-Start:       $remote_fs $network $syslog
# Required_Stop:        $remote_fs $syslog
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    Simple script to start a program at boot
# Description:          Rover Mobility Server
### END INIT INFO

from socket import *
from datetime import datetime
import time
import pygame
#import RPi.GPIO as GPIO
import numpy as np
import sys
import os

# System setup wait
time.sleep(5)

# Arduino address and connection info
address = ("192.168.1.178", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

# Initialize pygame and joysticks
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.joystick.init()

'''
# LED status signals
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
redLed = 18
greenLed = 23
blueLed = 24
GPIO.setup(redLed, GPIO.OUT)  # Red LED
GPIO.setup(greenLed, GPIO.OUT)  # Green LED
GPIO.setup(blueLed, GPIO.OUT)  # Blue LED
'''

#Global declarations
global paused
global controlString
global controls  # Holds file configurations
global modeNum  # Current mode index to toggle modeNames lst
global mode  # Current set name (string) in use
global modeNames  # List of set names (strings) from .txt file
global actionTime  # Seconds needed to trigger pause / mode change
global pausedLEDs  # LED settings for paused mode
paused = False
modeNum = 0
actionTime = 3
pausedLEDs = { "R" : True, "G" : False, "B" : False }  # Red for paused

actionList = ["motor1", "motor2", "arm2", "arm3", "joint1", "joint4", "joint5a",
              "joint5b", "reserved1", "ledMode"]  # List in order of socket output values

global roverActions
def setRoverActions():
    global roverActions
    roverActions =  {
              "motor1":    {"special": "motor", "rate": "motor", "direction": 1, "value": 0},
              "motor2":    {"special": "motor", "rate": "motor", "direction": 1, "value": 0},
              "arm3":      {"special": "motor", "rate": "none", "direction": 1, "value": 0},
              "joint1":    {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "arm2":      {"special": "motor", "rate": "none", "direction": 1, "value": 0},
              "joint4":    {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "joint5a":   {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "joint5b":   {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "reserved1": {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "ledMode":   {"special": "none", "rate": "none", "direction": 1, "value": 0}}
    # Not rover actions, but stored in same location. These actions trigger events within this module
    roverActions["pause"] = {"held": False, "direction": 1, "value": 0, "set": 0}  # Added to support "pause" action
    roverActions["mode"] = {"held": False, "direction": 1, "value": 0}  # Added to support "mode" action
    roverActions["throttle"] = {"direction": 1, "value": 0.5}  # Throttle value for "motor" rate multiplier (-1 to 1)
    roverActions["throttleStep"] = {"held": False, "direction": 1, "value": 0}  # Added to support button throttle

setRoverActions()  # Initiate roverActions to enter loop

# Initialize connection to Arduino
client_socket.sendto(bytes("0,0,0,0,0,0,0,0,0,1", "utf-8"), address)

def startUp(argv):
    global controlString, controls, modeNames, mode, roverActions
    fileName = "rumblepad.txt"
    if len(sys.argv) == 2:
        fileName = str(sys.argv[1])
    elif len(sys.argv) > 2:
        print("Exceeded arguments")
        sys.exit()
    try:
        controlString = open(fileName).read().replace('\n', '').replace('\r', '')
    except IOError:
        print ("Unable to open file")
        sys.exit()
    controls = eval(controlString)
    modeNames = list(sorted(controls.keys()))
    mode = modeNames[modeNum]  # mode 0 = both, mode 1 = mobility, mode 2 = arm
    roverActions["mode"]["set"] = modeNum
    roverActions["ledMode"]["value"] = controls[mode]["ledCode"]
    #setLed()

def stop():
    global paused
    paused = True

# Helper funcs for rate multipliers. Funcs take zero, one, or more arguments as needed
def getZero(*arg):
    return 0

def getOne(*arg):
    return 1

''' Direction: in case axis needs to be reversed
    Should always return value between -1 and 1 '''
def getRate():
    return roverActions["throttle"]["direction"] * roverActions["throttle"]["value"]

specialMultipliers = {"motor": 127, "none": 1}
rateMultipliers = {"motor": getRate, "none": getOne}

def throttleStep():
    global roverActions
    if (not roverActions["throttleStep"]["held"] and roverActions["throttleStep"]["value"]):  # New button press
        roverActions["throttleStep"]["held"] = True
        throttle = round(roverActions["throttle"]["value"] * 10.0) / 10  # Round out analog value to tenths place
        change = roverActions["throttleStep"]["direction"] * roverActions["throttleStep"]["value"] * 0.2
        throttle += change
        if throttle < -0.6:
            throttle = -0.6
        if throttle > 0.8:
            throttle = 0.8
        roverActions["throttle"]["value"] = throttle
    if (roverActions["throttleStep"]["held"] and not roverActions["throttleStep"]["value"]):  # Button held, but released
        roverActions["throttleStep"]["held"] = False

def computeSpeed(key):
    val = roverActions[key]
    throttleValue = rateMultipliers[val["rate"]]()  # Get current rate multiplier (-1 to +1), calls getRate or getOne accordingly
    calcThrot = np.interp(throttleValue, [-1 , 1], [0, 1])
    speed = int(specialMultipliers[val["special"]] * calcThrot * val["direction"] * val["value"])
    return speed

'''
def setLed():
    if paused:
        myLeds = pausedLEDs
    else:
        myLeds = controls[mode]["leds"]
    GPIO.output(redLed,GPIO.HIGH) if myLeds["R"] else GPIO.output(redLed,GPIO.LOW)
    GPIO.output(greenLed,GPIO.HIGH) if myLeds["G"] else GPIO.output(greenLed,GPIO.LOW)
    GPIO.output(blueLed,GPIO.HIGH) if myLeds["B"] else GPIO.output(blueLed,GPIO.LOW)
'''

def checkPause():
    global paused, roverActions
    if (not roverActions["pause"]["held"] and roverActions["pause"]["value"]):  # New button press
        roverActions["pause"]["held"] = True
        roverActions["pause"]["lastpress"] = datetime.now()
    if (roverActions["pause"]["held"] and not roverActions["pause"]["value"]):  # Button held, but now released
        roverActions["pause"]["held"] = False
    if (roverActions["pause"]["held"] and roverActions["pause"]["value"] and (
        datetime.now() - roverActions["pause"]["lastpress"]).seconds >= actionTime):  # Button held for required time
        roverActions["pause"]["lastpress"] = datetime.now()  # Keep updating time as button may continue to be held
        paused = not paused

def checkModes():
    global modeNum, mode, roverActions
    if (not roverActions["mode"]["held"] and roverActions["mode"]["value"]):  # New button press
        roverActions["mode"]["held"] = True
        roverActions["mode"]["lastpress"] = datetime.now()
    if (roverActions["mode"]["held"] and not roverActions["mode"]["value"]):  # Button held, but now released
        roverActions["mode"]["held"] = False
    if (roverActions["mode"]["held"] and roverActions["mode"]["value"] and (datetime.now() - roverActions["mode"][
        "lastpress"]).seconds >= actionTime and not paused):  # Button held for required time
        roverActions["mode"]["lastpress"] = datetime.now()  # Keep updating time as button may continue to be held
        modeNum += 1
        if modeNum >= len(modeNames):
            modeNum = 0
        mode = modeNames[modeNum]
        setRoverActions()  # Clear all inputs
        roverActions["mode"]["set"] = modeNum
        roverActions["ledMode"]["value"] = controls[mode]["ledCode"]

def checkButtons():
    global roverActions
    events = pygame.event.get([ pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP ] )  # Only check buttons that have changed state
    for event in events:
        currentJoystick = pygame.joystick.Joystick(event.joy)
        name = pygame.joystick.Joystick(event.joy).get_name()
        joyForSet = controls[mode].get(name)  # Get joystick in current set
        if (joyForSet):
            typeForJoy = joyForSet.get("buttons")  # Get joystick control type
            if (typeForJoy):
                control_input = typeForJoy.get(event.button)  # Check if input defined for controller
                if (control_input):
                    val = currentJoystick.get_button(event.button)  # Read button value, assign to roverActions
                    roverActions[control_input[0]]["value"] = val
                    roverActions[control_input[0]]["direction"] = control_input[1]  # Set direction multiplier
    discard = pygame.event.get()

def checkAxes(currentJoystick):
    global roverActions
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):
        typeForJoy = joyForSet.get("axes")  # Get joystick control type
        if (typeForJoy):
            axes = currentJoystick.get_numaxes()
            for i in range(axes):
                control_input = typeForJoy.get(i)  # Check if input defined for controller
                if (control_input):
                    val = currentJoystick.get_axis(i)  # Read axis value, assign to roverActions
                    roverActions[control_input[0]]["value"] = val
                    roverActions[control_input[0]]["direction"] = control_input[1]  # Set direction multiplier

def checkHats(currentJoystick):
    global roverActions
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):
        typeForJoy = joyForSet.get("hats")  # Get joystick control type
        if (typeForJoy):
            count = currentJoystick.get_numhats()
            for x in range(count):
                val = currentJoystick.get_hat(x)  # Store hat value, needed more than once
                for y in range(len(val)):  # Get the number of controller values
                    # Input may be stored multiple times, check both
                    control_input = typeForJoy.get((x, y))  # Check if east/west defined
                    if (control_input):
                        roverActions[control_input[0]]["value"] = val[y]
                        roverActions[control_input[0]]["direction"] = control_input[1]  # Set direction multiplier

def main(*argv):
    global paused
    startUp(argv)  # Load appropriate controller(s) config file
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        pygame.joystick.Joystick(i).init()
    while True:
        pygame.event.pump()  # Keeps pygame in sync with system, performs internal upkeep
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            stop()
        checkButtons()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            checkAxes(joystick)
            checkHats(joystick)
            throttleStep()
            checkPause()
            checkModes()
            #setLed()
            print("Sending Arduino command")
            try:
                re_data = client_socket.recvfrom(512)
                print(bytes.decode(re_data[0]))  # Debug
                if bytes.decode(re_data[0]) == "r":
                    print("Received packet")  # Debug
                    if (paused):
                        outVals = list(map(getZero, actionList))
                    else:
                        outVals = list(map(computeSpeed, actionList)) # Output string determined by actionList[] order
                    outVals = list(map(str, outVals))
                    outString = ",".join(outVals)
                    client_socket.sendto(bytes(outString,"utf-8"), address)
                    print(outString)
            except:
                print("Send failed")
                pass

if __name__ == '__main__':
    main()
