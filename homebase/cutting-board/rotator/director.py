print("starting director")
from time import sleep
import sys
import math
import numpy as np
import socket
from struct import *
from threading import Thread
from decimal import Decimal
from deepstream import *
#import pyserial
import datetime
import subprocess
import re
import requests



# gnss connection info
__antenna_gps_address = "192.168.1.38", 3777
__antenna_gps_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
__antenna_gps_socket.settimeout(0.5)

#__rover_gps_address = ("place holder",9999) #gonna grab this from deepstream
#__rover_gps_socket = socket(AF_INET, SOCK_DGRAM)
#__antenna_gps_socket.settimeout(0.5)
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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 7075))
            s.listen(2)
            break
        except:
            print("Waiting For Connection")
            sleep(2)


    while True:
        try:
            conn, address = s.accept()
            print("Connection from", address)
            break
        except:
            print("ERROR CONNECTING")
            sleep(3)
        
    pattern = re.compile('(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
    print("Waiting for GPS Lock...")

    while True:
        try:
            data = conn.recv(2048)
            print(data)
            m = re.match(pattern, data)
            if m:
                payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/gps", 
                "data": {"lat": float(m.group(3)), "lon": float(m.group(4)),
                "altitude": float(m.group(5)), "fix": (True if (int(m.group(6)) > 0) else False),
                "nos": int(m.group(7)), "sdn":float(m.group(8)), 
                "sde": float(m.group(9)), "sdu":float(m.group(10)),
                "sdne":float(m.group(11)), "sdeu":float(m.group(12)),
                "sdun":float(m.group(13)), "age":float(m.group(14)), 
                "ratio":float(m.group(15)) }} ]}
                __antenna_gps = (payload["lat"] + payload["lon"])
                sys.stdout.write(payload["lat"] + payload["lon"])   
                #sys.stdout.write(m.group(1) + ' ' + m.group(2) + ' ' + m.group(2) + ' '
                #+ m.group(3) + ' ' + m.group(4) + m.group(5) + ' ' + m.group(6) + ' ' 
                #+ m.group(7) + ' ' + m.group(8) + ' ' + m.group(9) + ' ' + m.group(10) + ' ' 
                #+ m.group(11) + ' '+ m.group(12) + ' '+ m.group(13) + ' ' + m.group(14) + ' '
                #+ m.group(15) + ' '+ '\n')
                    
            else:
                print("No valid regex data")
                s.close()
                break

            print(data)
        except KeyboardInterrupt:
            pass

    return __antenna_gps

def getRoverGPS():
    __rover_gps = (get('gps')['lat'], get('gps')['lon'])
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
    __antenna_heading = subprocess.check_output(["python3", "IMU_Acc_Mag_Gyro.py"])
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

#ard = Serial.serial(ARDUINO_PORT, BAUD_RATE)
#ard.open()
#rover_gps = __rover_gps_socket.recv(64)
#get antenna gps point from gnss
#antenna_gps = __antenna_gps_socket.recv(64) #grabs gps being sent from gnss module over network socket
print("running")
testheading = setHeading()
print("got heading")
print(testheading)



#setHeading()
#setHeadingDifference()
#setDeltaDirection()
#setShouldTurnClockwise()
