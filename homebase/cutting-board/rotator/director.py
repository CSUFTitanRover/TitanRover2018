import time
import sys
import math
import numpy as np
from socket import *
from struct import *
from threading import Thread
from decimal import Decimal
#import pyserial
import datetime
import subprocess


# gnss connection info
__antenna_gps_address = ("192.168.1.38", 3777)
__antenna_gps_socket = socket(AF_INET, SOCK_DGRAM)
__antenna_gps_socket.settimeout(0.5)

__rover_gps_address = ("place holder",9999)
__rover_gps_socket = socket(AF_INET, SOCK_DGRAM)
__antenna_gps_socket.settimeout(0.5)


__antenna_gps = (None, None)
__rover_gps = (None, None)
__antenna_heading = 0
__targetHeading = 0
__headingDifference = 0
__clockwise = None
__deltaDirection = 0
__paused = False
__stop = False
time.sleep(3)

def getAntennaGPS():

    return __antenna_gps

def getRoverGPS():
    return __rover_gps

def setTargetHeading(__antena_gps, __rover_gps):
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

    __targetHeading = compass_heading
    return __targetHeading
def setHeading():
    '''
    Description:
        Retrieves current heading from IMU subprocess
    Args:
        None
    Returns:
        heading
    '''
    print("checking heading")
    __antenna_heading = subprocess.check_output(["python3", "test.py"])
    return __antenna_heading
def setHeadingDifference(__antenna_heading, __targetHeading):
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
def setDeltaDirection(__headingDifference):
    '''
    Description:
        Uses __headingDifference to retrieve positive representation of delta change, sets __deltaDirection
    Args:
        None
    Returns:
        Nothing
    '''
    __deltaDirection = abs(__headingDifference)

def setShouldTurnClockwise():
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

def main():


    ARDUINO_PORT = "/dev/ttyUSB0"
    BAUD_RATE = 9600
    #ard = Serial.serial(ARDUINO_PORT, BAUD_RATE)
    #ard.open()
    minPot = 0
    maxPot = 1023
    valPot = 511
    MARGIN_OF_ERROR = 5 #error of 5 degrees
    #rover_gps = __rover_gps_socket.recv(64)
    #get antenna gps point from gnss
    #antenna_gps = __antenna_gps_socket.recv(64) #grabs gps being sent from gnss module over network socket
    testheading = setHeading()
    print("got heading")
    print(testheading)



    #setHeading()
    #setHeadingDifference()
    #setDeltaDirection()
    #setShouldTurnClockwise()
    return heading