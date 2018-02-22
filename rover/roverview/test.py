from time import sleep
from rviewer import *

import time
startTime = int(round(time.time()))

myViewer = Viewer()

with open("rover_output_1517607156.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
#    def refreshScreen(self, motor1, motor2, facingAngle, dist, ang, direction):

startTime = int(round(time.time()))
firstTime = int(int(content[0].split(" ")[8])) # get the first time in the file

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
---------------------------------------------
destWaypoint:  (33.880468421, -117.882201079)
currentGPS:  (33.880408578, -117.88221536)
0 dist(cm):  678.3576189174986
1 currentHeading:  1.0625
2 targetHeading:  11.206344725566964
3 deltaDirection:  10.143844725566964
4 motor1:  63
5 motor2:  45
6 clockwise:  True
7 headingDiff:  10.143844725566964
8 time:  1517602236
---------------------------------------------

def refreshScreen(self, motor1, motor2, facingAngle, targetDistance, targetAngle, shouldCW):
'''

for x in content:
    #curTime = int(round(time.time())) - startTime
    #nextTime = int(int(x.split(" ")[8])) - firstTime
    #while(curTime < nextTime):
    #    curTime = int(round(time.time())) - startTime
    sleep(0.3)
    b = x.split(" ")
    myViewer.refreshScreen( float(b[4]), float(b[5]), float(b[1]), float(b[0]), getHeadingDifference(float(b[1]), float(b[2])), getTFFromString(b[6]) )