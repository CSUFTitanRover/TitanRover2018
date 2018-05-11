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
from struct import *
from datetime import datetime
import re
from subprocess import Popen, PIPE
from threading import Thread
from time import sleep, time
from serial import Serial
import pygame
import numpy as np
import sys
import os
from deepstream import post, get
from relayFunctions import ep
from leds import writeToBus

uname = str(Popen([ 'uname', '-m' ], stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8'))

isPi = True if (uname == 'armv7l\n' or uname == 'arm6l\n') else False
isNvidia = True if uname == 'aarch64\n' else False
serDevice = '/dev/serial/by-id/usb-Silicon_Labs_titan_rover_433-if00-port0'

# MHz initialization
mhzPiRelaySocket = None
try:
    mhzPiRelaySocket = socket(AF_INET, SOCK_STREAM)  #check - why is the mhz on tcp wont this lag the connection when it is having connection issues
    try: 
        mhzPiRelaySocket.connect(('192.168.1.5', 9005))
    except:
        print("mhzPiRelaySocket.connect((192.168.1.5, 9005) at start failed...")
        #ser = Serial(serDevice, 9600)
        #print(ser.is_open)
except:
    print("socket(AF_INET, SOCK_STREAM) at start failed...")

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
sleep(5)

'''
# Tx2 address and connection info - UPD connection
address = ('192.168.1.2', 5001)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)
'''

# Arduino address and connection info
try:
    address = ('192.168.1.10', 5000)
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(0.5)
except:
    print("arduino connection at start failed...")

# Initialize pygame and joysticks
os.environ['SDL_VIDEODRIVER'] = 'dummy'  #pygame will error since we don't use a video source, prevents that issue
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
global maxRotateSpeed
global turnInPlace
paused = False
modeNum = 0
actionTime = 3
maxRotateSpeed = 50
turnInPlace = None
pausedLEDs = { 'R' : True, 'G' : False, 'B' : False }  # Red for paused

actionList = ['motor1', 'motor2', 'arm2', 'arm3', 'joint1', 'joint4', 'joint5a',
              'joint5b', 'reserved1', 'ledMode']  # List in order of socket output values

global roverActions
def setRoverActions():
    global roverActions
    roverActions =  {
              'motor1':    {'special': 'motor', 'rate': 'motor', 'direction': 1, 'value': 0},
              'motor2':    {'special': 'motor', 'rate': 'motor', 'direction': 1, 'value': 0},
              'arm3':      {'special': 'motor', 'rate': 'none', 'direction': 1, 'value': 0},
              'joint1':    {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0},
              'arm2':      {'special': 'motor', 'rate': 'none', 'direction': 1, 'value': 0},
              'joint4':    {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0},
              'joint5a':   {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0},
              'joint5b':   {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0},
              'reserved1': {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0},
              'ledMode':   {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0}}
    # Not rover actions, but stored in same location. These actions trigger events within this module
    roverActions['pause'] = {'held': False, 'direction': 1, 'value': 0, 'set': 0}  # Added to support 'pause' action
    roverActions['mode'] = {'held': False, 'direction': 1, 'value': 0}  # Added to support 'mode' action
    roverActions['throttle'] = {'direction': 1, 'value': 0.0}  # Throttle value for 'motor' rate multiplier (-1 to 1)
    roverActions['throttleStep'] = {'held': False, 'direction': 1, 'value': 0}  # Added to support button throttle
    roverActions['rotate'] = {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0}  # Added to support turn in place
    #roverActions['auto'] = {'held': False, 'direction': 1, 'value': 0, 'set': 0}  # Added to support 'autoManual' mode

setRoverActions()  # Initiate roverActions to enter loop

# Initialize connection to Arduino
client_socket.sendto(bytes('0,0,0,0,0,0,0,0,0,1', 'utf-8'), address)

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
    roverActions['mode']['set'] = modeNum
    roverActions['ledMode']['value'] = controls[mode]['ledCode']
    setLed()

def stop():
    global paused
    paused = True

def getZero(*arg):
    return 0

def getOne(*arg):
    return 1

def getRate():
    return roverActions['throttle']['direction'] * roverActions['throttle']['value']  # If axis needs to be reversed

specialMultipliers = {'motor': 127, 'none': 1}
rateMultipliers = {'motor': getRate, 'none': getOne}

def throttleStep():
    global roverActions
    if (not roverActions['throttleStep']['held'] and roverActions['throttleStep']['value']):  # New button press
        roverActions['throttleStep']['held'] = True
        throttle = round(roverActions['throttle']['value'] * 10.0) / 10  # Round out analog value to tenths place
        change = roverActions['throttleStep']['direction'] * roverActions['throttleStep']['value'] * 0.2
        throttle += change
        if throttle < -0.6:
            throttle = -0.6
        if throttle > 0.8:
            throttle = 0.8
        roverActions['throttle']['value'] = throttle
    if (roverActions['throttleStep']['held'] and not roverActions['throttleStep']['value']):  # Button held, but released
        roverActions['throttleStep']['held'] = False

def computeSpeed(key):
    val = roverActions[key]
    throttleValue = rateMultipliers[val['rate']]()  # Get current rate multiplier (-1 to +1), calls getRate or getOne accordingly
    calcThrot = np.interp(throttleValue, [-1 , 1], [0, 1])
    speed = int(specialMultipliers[val['special']] * calcThrot * val['direction'] * val['value'])
    return speed

def setLed():
    if paused:
        myLeds = pausedLEDs
    else:
        myLeds = controls[mode]['leds']
    if isPi:
        GPIO.output(redLed,GPIO.HIGH) if myLeds['R'] else GPIO.output(redLed,GPIO.LOW)
        GPIO.output(greenLed,GPIO.HIGH) if myLeds['G'] else GPIO.output(greenLed,GPIO.LOW)
        GPIO.output(blueLed,GPIO.HIGH) if myLeds['B'] else GPIO.output(blueLed,GPIO.LOW)

def checkPause():
    global paused, roverActions
    if (not roverActions['pause']['held'] and roverActions['pause']['value']):  # New button press
        roverActions['pause']['held'] = True
        roverActions['pause']['lastpress'] = datetime.now()
    if (roverActions['pause']['held'] and not roverActions['pause']['value']):  # Button held, but now released
        roverActions['pause']['held'] = False
    if (roverActions['pause']['held'] and roverActions['pause']['value'] and (
        datetime.now() - roverActions['pause']['lastpress']).seconds >= actionTime):  # Button held for required time
        roverActions['pause']['lastpress'] = datetime.now()  # Keep updating time as button may continue to be held
        paused = not paused

def checkModes():
    global modeNum, mode, roverActions
    if (not roverActions['mode']['held'] and roverActions['mode']['value']):  # New button press
        roverActions['mode']['held'] = True
        roverActions['mode']['lastpress'] = datetime.now()
    if (roverActions['mode']['held'] and not roverActions['mode']['value']):  # Button held, but now released
        roverActions['mode']['held'] = False
    if (roverActions['mode']['held'] and roverActions['mode']['value'] and (datetime.now() - roverActions['mode'][
        'lastpress']).seconds >= actionTime and not paused):  # Button held for required time
        roverActions['mode']['lastpress'] = datetime.now()  # Keep updating time as button may continue to be held
        modeNum += 1
        if modeNum >= len(modeNames):
            modeNum = 0
        mode = modeNames[modeNum]
        setRoverActions()  # Clear all inputs
        roverActions['mode']['set'] = modeNum
        roverActions['ledMode']['value'] = controls[mode]['ledCode']

def checkButtons(currentJoystick):
    global roverActions
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):
        typeForJoy = joyForSet.get('buttons')  # Get joystick control type
        if (typeForJoy):
            buttons = currentJoystick.get_numbuttons()
            for i in range(buttons):
                control_input = typeForJoy.get(i)  # Check if input defined for controller
                if (control_input):
                    val = currentJoystick.get_button(i)  # Read button value, assign to roverActions
                    if (val == 0 and roverActions[control_input[0]]['direction'] == control_input[1]) or val != 0:
                        roverActions[control_input[0]]['value'] = val
                        roverActions[control_input[0]]['direction'] = control_input[1]  # Set direction multiplier

def checkAxes(currentJoystick):
    global roverActions
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):
        typeForJoy = joyForSet.get('axes')  # Get joystick control type
        if (typeForJoy):
            axes = currentJoystick.get_numaxes()
            for i in range(axes):
                control_input = typeForJoy.get(i)  # Check if input defined for controller
                if (control_input):
                    val = currentJoystick.get_axis(i)  # Read axis value, assign to roverActions
                    roverActions[control_input[0]]['value'] = val
                    roverActions[control_input[0]]['direction'] = control_input[1]  # Set direction multiplier

def checkHats(currentJoystick):
    global roverActions
    name = currentJoystick.get_name()
    joyForSet = controls[mode].get(name)  # Get joystick in current set
    if (joyForSet):
        typeForJoy = joyForSet.get('hats')  # Get joystick control type
        if (typeForJoy):
            count = currentJoystick.get_numhats()
            for x in range(count):
                val = currentJoystick.get_hat(x)  # Store hat value, needed more than once
                for y in range(len(val)):  # Get the number of controller values
                    # Input may be stored multiple times, check both
                    control_input = typeForJoy.get((x, y))  # Check if east/west defined
                    if (control_input):
                        roverActions[control_input[0]]['value'] = val[y]
                        roverActions[control_input[0]]['direction'] = control_input[1]  # Set direction multiplier

def checkDsButton():
    global dsButton, roverActions
    if (not roverActions['auto']['held'] and roverActions['auto']['value']):  # New button press
        roverActions['auto']['held'] = True
        roverActions['auto']['lastpress'] = datetime.now()
    if (roverActions['auto']['held'] and not roverActions['auto']['value']):  # Button held, but now released
        roverActions['auto']['held'] = False
        dsButton = False
    if (roverActions['auto']['held'] and roverActions['auto']['value'] and (
        datetime.now() - roverActions['auto']['lastpress']).seconds >= actionTime):  # Button held for required time
        roverActions['auto']['lastpress'] = datetime.now()  # Keep updating time as button may continue to be held
        dsButton = True

def checkRotate():
    global turnInPlace
    if roverActions['rotate']['value'] !=0:
        turnInPlace = roverActions['rotate']['direction']

def turn(outVal):
    global turnInPlace
    if turnInPlace == 1:
        outVal[0]
        outVal[1] = maxRotateSpeed
    elif turnInPlace == -1:
        outVal[0]
        outVal[1] = -maxRotateSpeed
    turnInPlace = None
    return outVal

def main(*argv):
    global paused, mobiliyMode, ser
    startUp(argv)  # Load appropriate controller(s) config file
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        pygame.joystick.Joystick(i).init()

    while True:
        pygame.event.pump()  # Keeps pygame in sync with system, performs internal upkeep
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            stop()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            checkAxes(joystick)
            checkHats(joystick)
            checkButtons(joystick)
            throttleStep()
            checkRotate()
            checkPause()
            checkModes()
            setLed()

            if paused:
                outVals = list(map(getZero, actionList))
            else:
                outVals = turn(list(map(computeSpeed, actionList))) # Output string determined by actionList[] order
            outVals = list(map(str, outVals))
            outString = ','.join(outVals)

            # trying GHz
            try:
                re_data = client_socket.recvfrom(512)
                #print(bytes.decode(re_data[0]))  # Debug
                if bytes.decode(re_data[0]) == "r":
                    #print("Received packet")  # Debug
                    client_socket.sendto(bytes(outString,'utf-8'), address)
                    print(outString)

            # GHz failed, try mhz
            except:
                print("GHz failed... trying MHz")
                try:
                    o = outVals
                    t = round(time(), 3)
                    mhzBytePack = pack('s 10h d s', 'b'.encode('utf-8'), o[0], o[1], o[2], o[3], o[4], o[5], o[6], o[7], o[8],    3, t, '#'.encode('utf-8'))

                    mhzPiRelaySocket.sendto(mhzBytePack, ('192.168.1.5', 9005))
                    #ser.write(mhzBytePack) # packed bytes
                except:
                    print("MHz failed...")
                    mhzPiRelaySocket.close()              #check - doesn't this close need a delay before new socket
                    mhzPiRelaySocket = socket(AF_INET, SOCK_STREAM)      #check - shouldn't this be UDP
                    mhzPiRelaySocket.connect(('192.168.1.5', 9005))


if __name__ == '__main__':
    main(*argv)

