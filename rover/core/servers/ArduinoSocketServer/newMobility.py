######################################################################################
#   Filename: mobility.py
#   Description: Mobility script to operate Rover wheels and arm joints. Controllers 
#       mapped in individual text files to use with pygame. Uses sockets to communicate 
#       between machines - The primary line of communication is a GHz frequency and 
#       uses a MHz backup frequency.
######################################################################################

from socket import *
from struct import *
from datetime import datetime
from threading import Thread
from time import sleep
from serial import Serial
import pygame
import subprocess
import numpy as np
import sys
import os
#from leds import writeToBus # For local mobility

# MHz initialization
serDevice = '/dev/serial/by-id/usb-Silicon_Labs_titan_rover_433-if00-port0'
mhzPiRelaySocket = None
piConnData = ('192.168.1.5', 9005)
try:
    mhzPiRelaySocket = socket(AF_INET, SOCK_STREAM)
    try:
        mhzPiRelaySocket.connect(piConnData)
    except:
        print("mhzPiRelaySocket.connect(piConnData) at start failed...")
        subprocess.call('kill -9 $(lsof -t -i:9005)', shell=True)
except:
    print("socket(AF_INET, SOCK_STREAM) at start failed...")

# Tx2 address and connection info - UPD connection
tx2ConnData = ('192.168.1.2', 5002)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)
try:
    client_socket.bind(('', 5001))
except:
    subprocess.call('kill -9 $(lsof -t -i:5001)', shell=True)

'''
# Arduino address and connection info to send Ard cmds direct
try:
    address = ('192.168.1.10', 5000)
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(0.5)
except:
    print("arduino connection at start failed...")
# Initialize connection to Arduino
#client_socket.sendto(bytes('0,0,0,0,0,0,0,0,0,1', 'utf-8'), address)
'''

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
global ghzConnection
global ghzCountdown 
paused = False
modeNum = 0
actionTime = 3
maxRotateSpeed = 70
turnInPlace = None
ghzConnection = True
ghzCountdown = 10
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
    #roverActions['auto'] = {'held': False, 'direction': 1, 'value': 0, 'set': 0}  # Added to support 'autoManual' mode

setRoverActions()  # Initiate roverActions to enter loop

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
    #setLed()

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

def trackGhzConnection():
    global ghzCountdown, ghzConnection
    while True:
        if ghzConnection:
            ghzCountdown -= 1
            if ghzCountdown <= 0:
                ghzConnection = False
        sleep(1)

def reconnect():
    global ghzConnection
    while True:
        if not ghzConnection:
            resp = os.system("ping -c 5 " + "192.168.1.2")
            if resp == 0:
                ghzConnection = True
        #sleep(5) # Try to check connection again every 5 seconds - autonomous mode active during this time

Thread(target = trackGhzConnection).start()
Thread(target = reconnect).start()

def main(*argv):
    global paused, ser, mhzPiRelaySocket
    startUp(argv)  # Load appropriate controller(s) config file
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        pygame.joystick.Joystick(i).init()

    while True:
        pygame.event.pump()  # Keeps pygame in sync with system, performs internal upkeep
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("Plug in the joystick and restart genius")
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
            #outVals = list(map(str, outVals))
            #outString = ','.join(outVals)
            print(outVals)
            outbound = pack('9h', outVals[0], outVals[1], outVals[2], outVals[3], outVals[4], outVals[5], outVals[6], outVals[7], outVals[8])
            outboundMhz = pack('2b', outVals[0], outVals[1])

            # trying GHz
            # if sendto fails, except will be triggered
            try:
                if ghzConnection:
                    client_socket.sendto(outbound, tx2ConnData)
                    data = client_socket.recvfrom(512)[0]
                    if data.decode('utf-8') != 'xff':
                        raise RuntimeError()
                    ghzConnection = 10
                # if sending over MHz 
                
                else:
                    raise RuntimeError()
                '''
                client_socket.close()
                client_socket = socket(AF_INET, SOCK_DGRAM)
                client_socket.settimeout(0.5)
                '''

            except (KeyboardInterrupt, SystemExit):
                client_socket.close()
                mhzPiRelaySocket.close()
                raise

            except:
                print("GHz failed... trying MHz")
                # Closing/reopening GHz socket          # DO WE WANT TO CLOSE AND REOPEN GHZ SOCKET?
                try:
                    mhzPiRelaySocket.send(outboundMhz)
                    # Receive GPS and post to deepstream
                    currentGps = mhzPiRelaySocket.recv(512)
                    post({'rover/gps': (currentGps[0], currentGps[1])}, 'rover/gps')
                except:
                    print("MHz failed...")
                    mhzPiRelaySocket.close()              #check - doesn't this close need a delay before new socket
                    mhzPiRelaySocket = socket(AF_INET, SOCK_STREAM)      #check - shouldn't this be UDP
                    mhzPiRelaySocket.connect(piConnData)


if __name__ == '__main__':
    main()
