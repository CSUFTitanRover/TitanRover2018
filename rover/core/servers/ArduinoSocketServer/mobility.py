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
import RPi.GPIO as GPIO
import numpy as np
# WAIT FOR STUFF
# time.sleep(5)

#LED Signals for status
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
redLed = 18
greenLed = 23
blueLed = 24
GPIO.setup(redLed, GPIO.OUT) # Red LED
GPIO.setup(greenLed, GPIO.OUT) # Green LED
GPIO.setup(blueLed, GPIO.OUT) # Blue LED

# Initialize pygame and joysticks
pygame.init()
pygame.joystick.init()


# Arduino address and connection info
address = ("192.168.1.177", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
#client_socket.settimeout(0.5)

#Globals declarations
global paused
paused = False
global controls # File controller configurations
controls = ""
global modeNum # Current mode index into modeNames list 
modeNum = 0
global mode # Set key string from controls dictionary 
mode = ""
global modeNames # List of set key strings 
modeNames = None
global actionTime # Seconds needed to trigger pause / mode change
actionTime = 3  
global pausedLEDs # LED settings for paused mode
pausedLEDs = { "R" : True, "G" : False, "B" : False } # Red for paused

actionList = ["motor1", "motor2", "arm1", "arm2", "joint1", "joint5", "joint6",
              "joint7"]  # List in order of output values

def setRoverActions(): # Sets rover actions during each iteration of while loop
    return   {"motor1": {"special": "motor", "rate": "motor", "direction": 1, "value": 0},
              "motor2": {"special": "motor", "rate": "motor", "direction": 1, "value": 0},
              "arm2":   {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "joint1": {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "arm1":   {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "joint5": {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "joint6": {"special": "none", "rate": "none", "direction": 1, "value": 0},
              "joint7": {"special": "none", "rate": "none", "direction": 1, "value": 0}}
global roverActions
roverActions = setRoverActions()

# Not rover actions, but stored in same location. These actions trigger events within this module
roverActions["pause"] = {"held": False, "direction": 1, "value": 0, "set": 0}  # Added to support "pause" action
roverActions["mode"] = {"held": False, "direction": 1, "value": 0}  # Added to support "mode" action
roverActions["throttle"] = {"direction": 1, "value": 0.5}  # Throttle value for "motor" rate multiplier (-1 to 1)
roverActions["throttleStep"] = {"held": False, "direction": 1, "value": 0} # Added to support "throttle"  

controlString = open("controls2.txt").read().replace('\n', '').replace('\r', '')
controls = eval(controlString)
modeNames = list(sorted(controls.keys()))
mode = modeNames[modeNum]  # mode 0 = both, mode 1 = mobility, mode 2 = arm

# Initialize connection to Arduino
data = (0,0,0,0,0,0,0,0,0,0)
client_socket.sendto(bytes(data, "utf-8"), address)

# Helper funcs for rate multipliers
def getZero(*arg): 
    return 0

def getOne(*arg):
    return 1

''' Direction: in case axis needs to be reversed
    Should always return positive value between 0 and 1 '''
def getRate():  
    return roverActions["throttle"]["direction"] * roverActions["throttle"]["value"]

specialMultipliers = {"motor": 127, "none": 1}  # Can we handle on Arduino side?
rateMultipliers = {"motor": getRate, "none": getOne}  # Can add more as needed, used in definition of type

def throttleStep():
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
    throttleValue = rateMultipliers[val["rate"]]()  # Get current rate multiplier (-1 to +1)
    calcThrot = np.interp(throttleValue, [-1 , 1], [0, 1]) # Interpolate value
    return int(specialMultipliers[val["special"]] * calcThrot * val["direction"] * val["value"])

''' This function changes the color of the LED on the Pi, based off of the current mode the rover is in
    Green meaning BOTH Mobility and Arm are active
    Blue meaning ONLY Mobility is active
    Purple meaning ONLY Arm is active
    Red meaning NEITHER Mobility or Arm is actice, we are in a paused state
    Input: NONE
    Output: NONE '''
def setLed():
    print("LED set")
    if paused:
        myLeds = pausedLEDs
    else:
        myLeds = controls[mode]["leds"]
    GPIO.output(redLed,GPIO.HIGH) if myLeds["R"] else GPIO.output(redLed,GPIO.LOW)
    GPIO.output(greenLed,GPIO.HIGH) if myLeds["G"] else GPIO.output(greenLed,GPIO.LOW)
    GPIO.output(blueLed,GPIO.HIGH) if myLeds["B"] else GPIO.output(blueLed,GPIO.LOW)

def stop():
    global paused
    paused = True
    print("STOPPED")

def checkPause():
    global paused
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
    global modeNum, mode 
    if (not roverActions["mode"]["held"] and roverActions["mode"]["value"]):  # New button press
        roverActions["mode"]["held"] = True
        roverActions["mode"]["lastpress"] = datetime.now()
    if (roverActions["mode"]["held"] and not roverActions["mode"]["value"]):  # Button held, but now released
        roverActions["mode"]["held"] = False
    if (roverActions["mode"]["held"] and roverActions["mode"]["value"] and (datetime.now() - roverActions["mode"][
        "lastpress"]).seconds >= actionTime):  # Button held for required time
        roverActions["mode"]["lastpress"] = datetime.now()  # Keep updating time as button may continue to be held
        modeNum += 1
        if modeNum >= len(modeNames):  
            modeNum = 0
        mode = modeNames[modeNum]
        roverActions["mode"]["set"] = modeNum

''' 
This function takes in a joystick, reads axes, and sets corresponding motor values to be sent to ESC.
Input: Joystick
Output: None
'''
def checkAxes(currentJoystick):
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

# This function takes in a joystick, checks state of buttons, and sets corresponding Rover commands.
#   Input: Joystick
#   Output: None
#   Buttons correspond to:
#   Joint 5.1   Rotate End Effector Left
#   Joint 4     Move Up
#   Joint 5.1   Rotate End Effector Right
#   Joint 4     Move Down
#   Joint 5.2   Close End Effector
#   Joint 5.2   Open End Effector
def checkButtons(currentJoystick):
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):  # 
        typeForJoy = joyForSet.get("buttons")  # Get joystick control type 
        if (typeForJoy):
            count = currentJoystick.get_numbuttons()
            for i in range(count):
                control_input = typeForJoy.get(i)  # Check if input defined for controller
                if (control_input): 
                    val = currentJoystick.get_button(i)  # Read axis value, assign to roverActions
                    roverActions[control_input[0]]["value"] = val  
                    roverActions[control_input[0]]["direction"] = control_input[1]  # Set direction multiplier

# This function takes in a joystick, checks state of hats, and sets corresponding values to manipulates Joint1.
#   Input: Joystick
#   Output: None
def checkHats(currentJoystick):
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):  
        typeForJoy = joyForSet.get("hats")  # Get joystick control type
        if (typeForJoy):  
            count = currentJoystick.get_numhats()  
            for x in range(count):
                val = joystick.get_hat(x)  # Get hat value ahead of time, needed more than once 
                for y in range(len(val)):  # Get the number of controller things
                    # Input may be stored multiple times, check both
                    control_input = typeForJoy.get((x, y))  # Check if east/west defined
                    if (control_input):
                        roverActions[control_input[0]]["value"] = val[y]
                        roverActions[control_input[0]]["direction"] = control_input[1]  # Set direction multiplier

while (1):
    setLed()
    for event in pygame.event.get():  # User-initiated
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        
    joystick_count = pygame.joystick.get_count()  # Get joystick count, send rover stop command if none
    if joystick_count == 0:
        stop()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        checkAxes(joystick)
        checkButtons(joystick)
        checkHats(joystick)
    throttleStep()
    checkPause()
    checkModes()

    try:
        re_data = client_socket.recvfrom(512)
        print(bytes.decode(re_data[0]))  # Debug
        if bytes.decode(re_data[0]) == "r":
            print("Received packet")     # Debug
            if (paused):  # Output string determined by actionList[] order
                outVals = list(map(getZero, actionList))
            else:
                outVals = list(map(computeSpeed, actionList))
            outVals = list(map(str, outVals))
            outString = ",".join(outVals)
            client_socket.sendto(bytes(outString,"utf-8"), address)
            print(outString)
    except:
        print("Send failed")
        pass 
