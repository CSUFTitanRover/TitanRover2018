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
import subprocess
from subprocess import Popen
from threading import Thread
from deepstream import post, get
import time
import pygame
import numpy as np
import sys
import os

uname = str(Popen([ "uname", "-m" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8"))
isPi = True if (uname == "armv7l\n" or uname == "arm6l\n") else False
isNvidia = True if uname == "arm64\n" else False




if isPi:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    redLed = 18
    greenLed = 23
    blueLed = 24
    GPIO.setup(redLed, GPIO.OUT)  # Red LED
    GPIO.setup(greenLed, GPIO.OUT)  # Green LED
    GPIO.setup(blueLed, GPIO.OUT)  # Blue LED

# System setup wait
time.sleep(5)

# Arduino address and connection info
address = ("192.168.1.10", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

# Initialize pygame and joysticks
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.joystick.init()

#Global declarations
global paused
global controlString
global controls  # Holds file configurations
global modeNum  # Current mode index to toggle modeNames lst
global mode  # Current set name (string) in use
global modeNames  # List of set names (strings) from .txt file
global actionTime  # Seconds needed to trigger pause / mode change
global pausedLEDs  # LED settings for paused mode
global dsMode  # Deepstream mode 
global dsButton
paused = False
modeNum = 0
actionTime = 3
dsMode = "manual"  
dsButton = False
pausedLEDs = { "R" : True, "G" : False, "B" : False }  # Red for paused

while True:
    success = None
    try:
        success = post({"mode": dsMode}, "mode")
    except:
        pass
    time.sleep(.1)
    if success == "SUCCESS":
        break


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
    roverActions["auto"] = {"held": False, "direction": 1, "value": 0, "set": 0}  # Added to support "autoManual" mode

setRoverActions()  # Initiate roverActions to enter loop

# Initialize connection to Arduino
def initArduinoConnection():
    client_socket.sendto(bytes("0,0,0,0,0,0,0,0,0,1", "utf-8"), address)
initArduinoConnection()

def startUp(argv):
    global controlString, controls, modeNames, mode, roverActions
    fileName = "logitech3dReset.txt"
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
    setLed()

def stop():
    global paused
    paused = True

# Helper funcs for rate multipliers. Funcs take zero, one, or more arguments as needed
def getZero(*arg):
    return 0

def getOne(*arg):
    return 1

def getRate():
    return roverActions["throttle"]["direction"] * roverActions["throttle"]["value"]  # If axis needs to be reversed

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

def setLed():
    if paused:
        myLeds = pausedLEDs
    else:
        myLeds = controls[mode]["leds"]
    if isPi:
        GPIO.output(redLed,GPIO.HIGH) if myLeds["R"] else GPIO.output(redLed,GPIO.LOW)
        GPIO.output(greenLed,GPIO.HIGH) if myLeds["G"] else GPIO.output(greenLed,GPIO.LOW)
        GPIO.output(blueLed,GPIO.HIGH) if myLeds["B"] else GPIO.output(blueLed,GPIO.LOW)

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

def checkDsButton():
    global dsButton, roverActions
    if (not roverActions["auto"]["held"] and roverActions["auto"]["value"]):  # New button press
        roverActions["auto"]["held"] = True
        roverActions["auto"]["lastpress"] = datetime.now()
    if (roverActions["auto"]["held"] and not roverActions["auto"]["value"]):  # Button held, but now released
        roverActions["auto"]["held"] = False
        dsButton = False
    if (roverActions["auto"]["held"] and roverActions["auto"]["value"] and (
        datetime.now() - roverActions["auto"]["lastpress"]).seconds >= actionTime):  # Button held for required time
        roverActions["auto"]["lastpress"] = datetime.now()  # Keep updating time as button may continue to be held
        dsButton = True

def sendToDeepstream():
    global dsMode
    while True:
        try:
            post({"mobilityTime": int(time.time())}, "mobilityTime")
            time.sleep(.1)
            m = get("mode")
            if type(m) == dict:
                dsMode = m["mode"]
        except:
            print("Cannot send to Deepstream") 
        time.sleep(.1)

def requestControl():
    try:
        modeRecord = post({"mode": "manual"}, "mode")
        print("Updated mode record:", str(modeRecord))
        time.sleep(.1)
        initArduinoConnection()
        print("Trying to initialize a connection to the arduino...")
    except:
        print("Cannot access mode record")
        
def main(*argv):
    global paused, dsButton, dsMode
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
            checkDsButton()
            if dsButton:
                requestControl()
            setLed()
            print("Sending Arduino command")
            try:
                re_data = client_socket.recvfrom(512)
                #print(bytes.decode(re_data[0]))  # Debug
                if bytes.decode(re_data[0]) == "r":
                        #print("Received packet")  # Debug
                    if paused:
                        outVals = list(map(getZero, actionList))
                    else:
                        outVals = list(map(computeSpeed, actionList)) # Output string determined by actionList[] order
                    outVals = list(map(str, outVals))
                    outString = ",".join(outVals)
                    if dsMode == "manual":
                        client_socket.sendto(bytes(outString,"utf-8"), address)
                        print(outString)
                    else:
                        print("Not in manual mode")
            except:
                print("Send failed")
               
if __name__ == '__main__':
    t1 = Thread(target = main)
    t2 = Thread(target = sendToDeepstream)
    t1.start()
    t2.start()
