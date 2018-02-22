from time import sleep
from deepstream import get
from rviewer import *

import time
startTime = int(round(time.time()))

myViewer = Viewer()

def shouldTurnClockwise(heading, targetHeading):
    myDict = {}
    myDict[abs(targetHeading - heading)] = targetHeading - heading
    myDict[abs(targetHeading - heading + 360)] = targetHeading - heading + 360
    myDict[abs(targetHeading - heading - 360)] = targetHeading - heading - 360
    b = myDict[min(myDict.keys())]
    return True if b > 0 else False

def getHeadingDifference(heading, targetHeading):  # Double check (0, 180)
    headingDifference = (targetHeading - heading + 180) % 360 - 180
    return headingDifference + 360 if headingDifference < -180 else headingDifference

def getTFFromString(str):
    return True if str == "True" else False


'''
post({"motor1": self.motor1, "motor2": self.motor2, "currentHeading": self.heading, "targetDistance": self.distance,
      "targetHeading": self.targetHeading, "shouldCW": self.clockwise}, "roverViz")
'''
while True:
    sleep(0.3)
    data = {}
    try:
        data = get("roverViz")  # get data payload
    except:
        print("rViz could not get deepstream data")
    #Then break it out into components and convert types as necessary.
    motor1 = float(data["motor1"])
    motor2 = float(data["motor2"])
    currentHeading = float(data["currentHeading"])
    targetDistance = float(data["targetDistance"])
    targetHeading = float(data["targetHeading"])
    shouldCW = getTFFromString(str(data["shouldCW"]))
    headDiff = getHeadingDifference(currentHeading, targetHeading)

    myViewer.refreshScreen(motor1, motor2, currentHeading, targetDistance, headDiff, targetHeading, shouldCW)