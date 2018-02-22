from time import sleep
from deepstream import get
from rviewer import *

import time
startTime = int(round(time.time()))

myViewer = Viewer()

def getHeadingDifference(heading, targetHeading):  # Double check (0, 180)
    headingDifference = (targetHeading - heading + 180) % 360 - 180
    return headingDifference + 360 if headingDifference < -180 else headingDifference

def getTFFromString(str):
    return True if str == "True" else False

lastWaypoint, arrival = None
while True:
    sleep(0.3)
    data = {}
    try:
        data = get("roverViz")  # get data payload
        arrival = get("arrival")
    except:
        print("rViz could not get deepstream data")
    if arrival and lastWaypoint and arrival["Waypoint"] != lastWaypoint:
        myViewer.flashArrivalMsg(arrival["Waypoint"], arrival["arrivalTime"])
    if data == {}:
        continue
    #Then break it out into components and convert types as necessary.
    motor1 = float(data["motor1"])
    motor2 = float(data["motor2"])
    currentHeading = float(data["currentHeading"])
    targetDistance = float(data["targetDistance"])
    targetHeading = float(data["targetHeading"])
    shouldCW = getTFFromString(str(data["shouldCW"]))
    headDiff = getHeadingDifference(currentHeading, targetHeading)

    myViewer.refreshScreen(motor1, motor2, currentHeading, targetDistance, headDiff, targetHeading, shouldCW)
