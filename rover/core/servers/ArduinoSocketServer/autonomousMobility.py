'''
    Autonomous mobility script
    Titan Rover 2018
    Chary Vielma - chary.vielma@csu.fullerton.edu
    Adapted from TitanRover2017 autonomous script
'''
from socket import *
from threading import Thread
import math
import sys
from time import sleep
from deepstream import post, get

import numpy as np

# Arduino address and connection info
address = ("192.168.1.178", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

global heading
global gps
global imu
global deltaDirection 
global clockwise
global distance 
global destinationWaypoint
global targetHeading
destinationWaypoint = (33.88210346, -117.88163178)
waypoints = [destinationWaypoint]

# For every x input (x == deltaDirection), y output returns speed
distanceX = [5, 15, 25]  
distanceY = [25, 42.5, 60] 
forwardX = [20, 60] 
forwardY = [25, 45] 

# Initialize connection to Arduino
client_socket.sendto(bytes("0,0,0,0,0,0,0,0,0,4", "utf-8"), address)

# If clockwise, return True, else return False (counterclockwise)
def shouldTurnClockwise(heading, targetHeading):
    if heading == targetHeading:
        return True if abs(heading - targetHeading) <= 180 else False 
    else:
        return False if abs(heading - targetHeading) < 180 else True

def getHeadingDifference(heading, targetHeading):  # Double check (0, 180)
    headingDifference = (targetHeading - heading + 180) % 360 - 180
    return abs(headingDifference + 360) if headingDifference < -180 else abs(headingDifference)

def getDeepstreamData():  # Thread 
    global imu, gps
    try:
        newGps = get("gps")
        gps = (newGps["lat"], newGps["lon"])
        imu = get("imu")["heading"]
    except:
        print("Deepstream failed")
    sleep(0.5)

# Calculates the target heading between two coordinates
def calculateHeading(currentWaypoint, nextWaypoint):  
    """
    Code adapted from https://gist.github.com/jeromer
    Calculates the heading between two points.
    The formula used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `currentWaypoint: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `nextWaypoint: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The heading in degrees
    :Returns Type:
      float
    """
    if (type(currentWaypoint) != tuple) or (type(nextWaypoint) != tuple):
        raise TypeError("Only tuples allowed")

    lat1 = math.radians(currentWaypoint[0])
    lat2 = math.radians(nextWaypoint[0])

    diffLong = math.radians(nextWaypoint[1] - currentWaypoint[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_heading = math.atan2(x, y)

    # Now we have the initial heading but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass heading
    # The solution is to normalize the initial heading as shown below
    initial_heading = math.degrees(initial_heading)
    compass_heading = (initial_heading + 360) % 360

    return compass_heading

# Haversine formula to calculate distance(cm) between two gps coordinates
def getDistance(origin, destination):
    print("getting into Distance")
    a1, b1 = origin
    a2, b2 = destination
    radius = 6371 # km

    da = math.radians(a2-a1)
    db = math.radians(b2-b1)
    a = math.sin(da/2) * math.sin(da/2) + math.cos(math.radians(a1)) \
        * math.cos(math.radians(a2)) * math.sin(db/2) * math.sin(db/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d * 1000

# Use deepstream thread and helper function calculateHeading to obtain current heading
def getHeading():
    global heading, gps, destinationWaypoint
    heading = calculateHeading(gps, destinationWaypoint)

def setMotors(motor1, motor2):
    try:
        re_data = client_socket.recvfrom(512)
        if bytes.decode(re_data[0]) == "r":
            outString = str(motor1) + "," + str(motor2) + ",0,0,0,0,0,0,0,4"
            client_socket.sendto(bytes(outString, "utf-8"), address)
            print(outString)
    except:
        print("Send failed")

# Stub - further implementation needed
def canProceed():
    print("Checking if able to proceed")
    return True

# Stub - further implementation needed
def generateNewWaypoints():
    global waypoints
    print("If obstacle, create new waypoints and add to waypoints list")
    
#def main():
t1 = Thread(target = getDeepstreamData)
t1.start()

while waypoints:
    destinationWaypoint = waypoints.pop(0)
    distance = getDistance(gps, destinationWaypoint)
    while(distance > 5):
        deltaDirection = getHeadingDifference(heading, targetHeading)
        clockwise = shouldTurnClockwise(heading, targetHeading)
        motor2 = int(np.interp(deltaDirection, distanceX, distanceY)) # Calculate rotational speed, decrease as target angle is reached
        motor1 = np.interp(distance, forwardX, forwardY) # Calculate linear speed, decrease as target is reached
        motor1 = int(motor1 * np.interp(deltaDirection,[0,180],[1,0])) # Multiply speed to decrease it the further off target we are pointing
        if deltaDirection < 5:
            motor2 = 0
        if not clockwise:
            motor2 = -motor2
        setMotors(motor1, motor2)
        distance = getDistance(gps, destinationWaypoint)

#if __name__ == 'main':
    #main()
