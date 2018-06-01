# Run with 'python3.5 joystickArmFreq.py science.txt' using rumblepad controller 

from datetime import datetime
from time import sleep
import pygame
import numpy as np
import sys
import os

# Initialize pygame and joysticks
os.environ['SDL_VIDEODRIVER'] = 'dummy'  #pygame will error since we don't use a video source, prevents that issue
pygame.init()
pygame.joystick.init()

# System setup wait
sleep(3)

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
maxRotateSpeed = 70
turnInPlace = None
pausedLEDs = { 'R' : True, 'G' : False, 'B' : False }  # Red for paused

actionList = ['motor1', 'motor2', 'arm2', 'arm3', 'joint1', 'joint4', 'joint5a',
              'joint5b', 'ledMode']  # List in order of socket output values


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
              'ledMode':   {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0}}
    # Not rover actions, but stored in same location. These actions trigger events within this module
    roverActions['pause'] = {'held': False, 'direction': 1, 'value': 0, 'set': 0}  # Added to support 'pause' action
    roverActions['mode'] = {'held': False, 'direction': 1, 'value': 0}  # Added to support 'mode' action
    roverActions['throttle'] = {'direction': 1, 'value': 0.0}  # Throttle value for 'motor' rate multiplier (-1 to 1)
    roverActions['throttleStep'] = {'held': False, 'direction': 1, 'value': 0}  # Added to support button throttle
    roverActions['rotate'] = {'special': 'none', 'rate': 'none', 'direction': 1, 'value': 0}  # Added to support turn in place

setRoverActions()  # Initiate roverActions to enter loop

def startUp():
    global controlString, controls, modeNames, mode, roverActions
    fileName = "science.txt"
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

def stop():
    global paused
    paused = True

def getZero(*arg):
    return 0

def getOne(*arg):
    return 1

def getRate():
    return roverActions['throttle']['direction'] * roverActions['throttle']['value']  # If axis needs to be reversed

specialMultipliers = {'motor': 60, 'none': 1}
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

def main():
    global paused
    startUp()  
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        pygame.joystick.Joystick(i).init()

    while True:
        pygame.event.pump()  # Keeps pygame in sync with system, performs internal upkeep
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("Plug in rumblepad and restart genius")
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

            if paused:
                outVals = list(map(getZero, actionList))
            else:
                outVals = turn(list(map(computeSpeed, actionList))) # Output string determined by actionList[] order
            
            print("Joint 1: ", outVals[4], " Joint 2: ", outVals[2], " Joint 4: ", outVals[5], " Joint 5.1: ", outVals[6])
            


if __name__ == '__main__':
    main()
    try:
        while True:
            print("main loop")
            sleep(0.01)
    except:
        print("Keyboard Interrupt...")
