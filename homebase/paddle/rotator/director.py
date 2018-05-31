print("starting director1")
from time import sleep
import sys
import math
import numpy as np
import socket
from struct import *
from threading import Thread
from decimal import Decimal
from deepstream import *
import datetime
import subprocess
import re
import requests
import serial

#Arduino Serial Out
ardName = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85439313330351D0E102-if00'
ardOut =  serial.Serial(ardName, 9600, timeout=None)

# gnss connection info
__antenna_gps_address = "192.168.1.31"
__antenna_gps_port = 7075
__antenna_gps_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
__antenna_gps_socket.settimeout(0.5)

__rover_gps = ('', '')

__antenna_gps = (None, None)
__rover_gps = (None, None)
__antenna_heading = 0
__targetHeading = 0
__headingDifference = 0
__clockwise = None
__deltaDirection = 0
__paused = False
__stop = False

def getAntennaGPS():
    while True:
        try:
            print("Initializing socket")
            __antenna_gps_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #this needs to be re-called in a loop when attempting to reconnect
        except:
            print("failed to initialize socket.")
            sleep(0.5)
            continue
        try:
            print("connecting")
            __antenna_gps_socket.connect((__antenna_gps_address, __antenna_gps_port))
            print("connected")
            break
        except:
            print("Failed to connect!")
            sleep(0.5)
            continue
    pattern = re.compile(b'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
    print("Waiting for GPS Lock...")

    try:
        data = __antenna_gps_socket.recv(2048)
        m = re.match(pattern, data)
        if m:
            __antenna_gps = (float(m.group(3)), float(m.group(4)))        
        else:
            print("No valid regex data")
            __antenna_gps_socket.close()
        print("received gps data from socket")
    except:
        print("error receiving antenna gps from socket")
        pass
    return __antenna_gps

def getRoverGPS():
    print("getting rover gps")
    data = get('gps', '192.168.1.8')
    print("got rover gps from deepstream")
    print(data)
    return (data["lat"], data["lon"])

def getTargetHeading(__antena_gps, __rover_gps):
    '''
    Description:
        Code adapted from https://gist.github.com/jeromer
        Calculates and sets __targetHeading given __antenna_gps and __rover_gps
    Args:
        two gps points: current, target
    Returns:
        heading to target
    '''
    if (type(__antenna_gps) != tuple) or (type(__rover_gps) != tuple):
        raise TypeError("Only tuples allowed")

    lat1 = math.radians(__antenna_gps[0])
    lat2 = math.radians(__rover_gps[0])

    diffLong = math.radians(__rover_gps[1] - __antenna_gps[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_heading = math.atan2(x, y)

    initial_heading = math.degrees(initial_heading)
    compass_heading = (initial_heading + 360) % 360
    return compass_heading
def getAntennaHeading():
    '''
    Description:
        Retrieves current heading from IMU subprocess
    Args:
        None
    Returns:
        heading
    '''
    print("checking heading")
    data = subprocess.check_output(["python3", "IMU_Acc_Mag_Gyro.py"])
    print("returning heading")
    return float(data)

 ############################################################## UNUSED
def getHeadingDifference(__antenna_heading, __targetHeading):
    '''
    Description:
        Calculates and sets __headingDifference to degress between __antenna_heading and __targetHeading
    Args:
        __antenna_heading, __targetHeading
    Returns:
        returns heading difference
    '''
    __headingDifference = (__targetHeading - __antenna_heading + 180) % 360 - 180
    __headingDifference = __headingDifference + 360 if __headingDifference < -180 else __headingDifference
    return __headingDifference
def getDeltaDirection(__headingDifference):
    '''
    Description:
        Uses __headingDifference to retrieve positive representation of delta change, sets __deltaDirection
    Args:
        None
    Returns:
        Nothing
    '''
    __deltaDirection = abs(__headingDifference)
    return __deltaDirection

def getShouldTurnClockwise():
    '''
    Description:
        Sets __clockwise to True if shorter turn is clockwise, else False for counterclockwise
    Args:
        None
    Returns:
        Nothing
    '''
    myDict = {}
    myDict[abs(__targetHeading - __antenna_heading)] = __targetHeading - __antenna_heading
    myDict[abs(__targetHeading - __antenna_heading + 360)] = __targetHeading - __antenna_heading + 360 
    myDict[abs(__targetHeading - __antenna_heading - 360)] = __targetHeading - __antenna_heading - 360 
    b = myDict[min(myDict.keys())]
    __clockwise = True if b > 0 else False
    return __clockwise
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^UNUSED

'''
__rover_gps = getRoverGPS()
print("rover gps")
print(__rover_gps)

__antenna_gps = getAntennaGPS()
print("antenna gps")
print(__antenna_gps)

__antenna_heading = getHeading()
print("got heading")
print(__antenna_heading)

__targetHeading = getTargetHeading(__antenna_gps, __rover_gps)
print("got target heading")
print(__targetHeading)

__headingDifference = getHeadingDifference(__antenna_heading, __targetHeading)
print("got heading difference")
print(__headingDifference)


__deltaDirection = getDeltaDirection(__headingDifference)
print("got delta direction")
print(__deltaDirection)

__clockwise = getShouldTurnClockwise()
print("got clock direction")
print(__clockwise)
#call all the functions because I can
'''


    #return (get('gps')['lat'], get('gps')['lon'])

while True:
    try:

        __antenna_heading = getAntennaHeading() #get antenna heading from imu
        print(__antenna_heading)
    #take the heading => multiply it by 1000 => round it off => convert it to an int => pack it into serial transmittable bytes => write those bytes to arduino
        break
    except:
        print("failed to get heading")
        continue
while True:
    try:
        print("write initial heading to ard")
        ardOut.write(pack('i', int((__antenna_heading * 1000))))
        break
    except:
        print('failed to write initial heading to ard')
        continue
try:
    while True:
        print("updating in 5")
        sleep(1)
        __antenna_gps = getAntennaGPS()
        print(__antenna_gps)
        print("got antenna gps")
        __rover_gps = getRoverGPS()
        print(__rover_gps)
        print("got rover gps")

        __targetHeading = getTargetHeading(__antenna_gps, __rover_gps) #these three should always be called together to get the correct heading for the most recent position of the rover relative to the antenna, the call to the antenna can be omitted after it is called once but what if something crazy happens and the antenna moves?
        print("got target heading")
        if __targetHeading > 180:
            __targetHeading -= 360
        if __targetHeading > (__antenna_heading - 90) and __targetHeading < (__antenna_heading + 90):
            ardOut.write(struct.pack("i", (__targetHeading * 1000))) #sending new heading for the arduino to go to using its pot as reference.
except:
    print("error in loop")

