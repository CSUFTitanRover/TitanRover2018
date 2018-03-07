from time import sleep
from deepstream import get
from rviewer import *

import time
startTime = int(round(time.time()))

myViewer = Viewer()

def getTFFromString(str):
    return True if str == "True" else False

try:
    first = get("arrival")
    lastWaypoint = first["Waypoint"]
except:
    lastWaypoint = {}
arrival = {}

while True:
    sleep(0.3)
    data = {}
    try:
        data = get("roverViz")  # get data payload
        arrival = get("arrival")
    except:
        print("rViz could not get deepstream data")
    if arrival != {}:
        if arrival["arrivalTime"] != "start":
            if arrival["Waypoint"] != lastWaypoint:
                myViewer.flashArrivalMsg(arrival["Waypoint"], arrival["arrivalTime"])
                lastWaypoint = arrival["Waypoint"]
    if data == {} or data == "NO_RECORD":
        continue
    #Then break it out into components and convert types as necessary.
    motor1 = int(data["motor1"])
    motor2 = int(data["motor2"])
    currentHeading = float(data["currentHeading"])
    targetDistance = float(data["targetDistance"])
    shouldCW = getTFFromString(str(data["shouldCW"]))
    headDiff = float(data["headingDifference"])
    myViewer.refreshScreen(motor1, motor2, currentHeading, targetDistance, headDiff, shouldCW)
