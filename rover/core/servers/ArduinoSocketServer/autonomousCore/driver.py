######################################################################################
#    Filename: driver.py
#    Description: Autonomous traversal module - TitanRover2018
#         Given a single GPS coordinate, the Rover will drive to this point (within a 
#         predetermined threshold). Driving occurs in a linear fashion. 
#         Given a heading and distance (cm), GPS coordinate will be generated and 
#         the Rover will drive to this point.
#         Give a heading, the Rover will rotate in place to face this direction. 
#         Adapted from TitanRover2017 autonomous script
######################################################################################
import time
import sys
import math
import numpy as np
from socket import *
from threading import Thread
from deepstream import post, get

MINFORWARDSPEED = 20
MAXFORWARDSPEED = 50
TARGETTHRESHOLD = 20  # In cm
CORRECTIONTHRESHOLD = 3.5  # In degrees
HEADINGTHRESHOLD = 3 # In degrees

class Driver:

    def __init__(self):

        # Arduino address and connection information
        self.__address = ("192.168.1.10", 5000)
        self.__client_socket = socket(AF_INET, SOCK_DGRAM)
        self.__client_socket.settimeout(0.5)
        self.__client_socket.sendto(bytes("0,0,0,0,0,0,0,0,0,4", "utf-8"), self.__address)

        # Tailered to Runt Rover
        self.__angleX = [5, 15, 25]
        self.__rotateY = [40, 50, 90]
        self.__distanceX = [60, 120]
        self.__speedY = [65, 110]

        '''
        self.__angleX = [5, 15, 25]
        self.__rotateY = [25, 42.5, 60]
        self.__distanceX = [20, 60]
        self.__speedY = [25, 45]
        '''

        self.__gps = (None, None)
        self.__nextWaypoint = (None, None)
        self.__heading = 0
        self.__targetHeading = 0
        self.__headingDifference = 0
        self.__clockwise = None
        self.__deltaDirection = 0
        self.__distance = 0
        self.__motor1 = 0
        self.__motor2 = 0
        self.__paused = False
        self.__stop = False
        time.sleep(3)
        
    def roverViewer(self):
        '''
        Description:
            Updates deepstream record 'roverViz' with motor1, motor2, currentHeading, 
            targetDistance, targetHeading, headingDiff, and clockwise values for the rover viewer.
        Args:
            None
        Returns:
            Nothing
        '''
        post({"motor1": self.__motor1, "motor2": self.__motor2, "currentHeading": self.__heading, "targetDistance": self.__distance, "deltaDirection": self.__deltaDirection, "shouldCW": self.__clockwise}, "roverViz")
        time.sleep(0.04)

    def setShouldTurnClockwise(self):
        '''
        Description:
            Sets self.__clockwise to True if shorter turn is clockwise, else False for counterclockwise
        Args:
            None
        Returns:
            Nothing
        '''
        myDict = {}
        myDict[abs(self.__targetHeading - self.__heading)] = self.__targetHeading - self.__heading
        myDict[abs(self.__targetHeading - self.__heading + 360)] = self.__targetHeading - self.__heading + 360 
        myDict[abs(self.__targetHeading - self.__heading - 360)] = self.__targetHeading - self.__heading - 360 
        b = myDict[min(myDict.keys())]
        self.__clockwise = True if b > 0 else False
    
    def setHeadingDifference(self):
        '''
        Description:
            Calculates and sets self.__headingDifference to degress between self.__heading and self.__targetHeading
        Args:
            None
        Returns:
            Nothing
        '''
        self.__headingDifference = (self.__targetHeading - self.__heading + 180) % 360 - 180
        self.__headingDifference = self.__headingDifference + 360 if self.__headingDifference < -180 else self.__headingDifference

    def setTargetHeading(self):
        '''
        Description:
            Code adapted from https://gist.github.com/jeromer
            Calculates and sets self.__targetHeading given self.__gps and self.__nextWaypoint
        Args:
            None
        Returns:
            Nothing
        '''
        if (type(self.__gps) != tuple) or (type(self.__nextWaypoint) != tuple):
            raise TypeError("Only tuples allowed")

        lat1 = math.radians(self.__gps[0])
        lat2 = math.radians(self.__nextWaypoint[0])

        diffLong = math.radians(self.__nextWaypoint[1] - self.__gps[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_heading = math.atan2(x, y)

        initial_heading = math.degrees(initial_heading)
        compass_heading = (initial_heading + 360) % 360

        self.__targetHeading = compass_heading

    def setDistance(self):
        '''
        Description:
            Haversine formula - Calculates and sets self.__distance (in cm) given self.__gps 
            and self.__nextWaypoint
        Args:
            None
        Returns:
            Nothing
        '''
        a1, b1 = self.__gps
        a2, b2 = self.__nextWaypoint
        radius = 6371 # km

        da = math.radians(a2-a1)
        db = math.radians(b2-b1)
        a = math.sin(da/2) * math.sin(da/2) + math.cos(math.radians(a1)) \
            * math.cos(math.radians(a2)) * math.sin(db/2) * math.sin(db/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        self.__distance = d * 100000

    def sendMotors(self):
        '''
        Description:
            Performs Arduino socket call with appropriate self.__motor1 and self.__motor2 motor values
        Args:
            None
        Returns:
            Nothing
        '''
        try:
            re_data = self.__client_socket.recvfrom(512)
            if bytes.decode(re_data[0]) == "r":
                outString = str(self.__motor1) + "," + str(self.__motor2) + ",0,0,0,0,0,0,0,4"
                self.__client_socket.sendto(bytes(outString, "utf-8"), self.__address)
        except:
            print("Arduino send failed")

    def setGps(self):
        '''
        Description:
            Retrieves current GPS location from deepstream, sets self.__gps 
        Args:
            None
        Returns:
            Nothing
        '''
        try:
            self.__gps = (get("gps")["lat"], get("gps")["lon"])
        except:
            print("GPS error")

    def setHeading(self):
        '''
        Description:
            Retrieves current heading from deepstream, sets self.__heading 
        Args:
            None
        Returns:
            Nothing
        '''
        try:
            self.__heading = get("imu")["heading"]
        except:
            print("Heading error")

    def setDeltaDirection(self):
        '''
        Description:
            Uses self.__headingDifference to retrieve positive representation of delta change, sets self.__deltaDirection
        Args:
            None
        Returns:
            Nothing
        '''
        self.__deltaDirection = abs(self.__headingDifference)

    def calculateMotors(self):
        '''
        Description:
            Uses self.__deltaDirection and self.__distance to calculate and set speed and turn values 
            for self.__motor1 and self.__motor2. 
        Args:
            None
        Returns:
            Nothing
        '''
        self.__motor2 = int(np.interp(self.__deltaDirection, self.__angleX, self.__rotateY))
        self.__motor1 = np.interp(self.__distance, self.__distanceX, self.__speedY) 
        self.__motor1 = int(self.__motor1 * np.interp(self.__deltaDirection,[3,30],[1,0])) # Scale speed the further off target Rover is pointing
        if not self.__clockwise:
            self.__motor2 = -self.__motor2


    def stop(self):
        '''
        Description:
            Used to exit the goTo function. 
        '''
        self.__stop = True

    def pause(self):
        '''
        Description:
            Suspends Rover movement until resume() is called. 
        '''
        self.__paused = True

    def resume(self):
        '''
        Description:
            Resumes Rover movement after being paused. 
        '''
        self.__paused = False

    def notifyArrival(self):
        '''
        Description:
            Updates deepstream record 'arrival' with self.__nextWaypoint and arrivalTime once 
            the destination has been reached. Flashes LED pattern for on board visual cue. 
        Args:
            None
        Returns:
            Nothing
        '''
        self.__motor1 = self.__motor2 = 0

        # Update deepstream
        arrivalTime = str(time.strftime("%I:%M:%S" ,time.localtime()))
        try:
            post({"Waypoint": str(self.__nextWaypoint), "arrivalTime": arrivalTime}, "arrival")
        except:
            print("Notify error")

        # Blink lights
        leds = [0, 1, 2]
        color = toggle = 0
        for i in range(20):  # Blink red, green, and blue for 5 seconds
            try:
                re_data = self.__client_socket.recvfrom(512)
                if bytes.decode(re_data[0]) == "r":
                    outString = "0,0,0,0,0,0,0,0,0," + str(color)
                    self.__client_socket.sendto(bytes(outString, "utf-8"), self.__address)
                    time.sleep(0.25)
                    toggle += 1
                    if toggle >= len(leds):
                        toggle = 0
                    color = leds[toggle]
            except:
                print("Arduino send failed")
        self.sendMotors()        

    def setMinMaxFwdSpeeds(self, min, max):
        '''
        Description:
            Method overwrites default speedY[min, max] speeds. Confined to MINFORWARDSPEED 
            and MAXFORWARDSPEED.
        Args:
            min (int): desired minimum forward speed, max (int): desired maximum forward speed
        Returns:
            Nothing
        '''
        if type(min) != int or type(max) != int:
            raise TypeError("Only integers allowed")
            pass

        if max > MAXFORWARDSPEED:
            max = MAXFORWARDSPEED
        if min < MINFORWARDSPEED:
            min = MINFORWARDSPEED
        self.__speedY = [min, max]
        
    def rotateToHeading(self, newHeading):
        '''
        Description:
            Given a desired heading, Rover will rotate in place until oriented in the given direction
            (within a predetermined threshold). 
        Args:
            heading (float): The desired heading the Rover will face.
        Returns:
            Nothing
        '''
        if type(newHeading) != float:
            raise TypeError("Only floats allowed")
            pass

        self.__distance = 0
        self.__targetHeading = newHeading
        self.setHeading()
        self.setHeadingDifference()
        self.setDeltaDirection()
        while self.__deltaDirection > HEADINGTHRESHOLD:
            self.setShouldTurnClockwise()
            self.calculateMotors()
            motor1 = 0
            self.sendMotors()
            time.sleep(0.02)
            self.setHeading()
            self.setHeadingDifference()
            self.setDeltaDirection()

    def goTo(self, point):
        '''
        Description:
            Given one GPS point, method will continuously update GPS, heading, distance, delta direction to reach point (within a predetermined threshold). Upon arrival, a deepstream record will be updated.
        Args:
            point (tuple): Destination waypoint in the form (lat, lon).
            Ex: ( lat (float), lon (float) )
        Returns:
            Nothing
        '''
        if type(point) != tuple:
            raise TypeError("Only tuples allowed")
            pass
        if type(point[0]) != float or type(point[1]) != float:
            raise TypeError("Only floats allowed as tuple values")
            pass

        self.__nextWaypoint = point
        self.setGps()
        self.setHeading()
        self.setDistance()

        while self.__distance > TARGETTHRESHOLD and not self.__stop:
            while self.__paused:
                pass
            self.setTargetHeading()
            self.setHeadingDifference()
            self.setDeltaDirection()
            self.setShouldTurnClockwise()
            self.calculateMotors()
            if self.__deltaDirection < CORRECTIONTHRESHOLD:
                self.__motor2 = 0
                self.__headingDifference = None
            self.sendMotors()
            self.roverViewer()

            '''
            # Debug print
            print("------------------------------------------------")
            print("destWaypoint: ", self.__nextWaypoint, "\ncurrentGPS: ", self.__gps, "\ndist(cm): ", self.__distance, "\ncurrentHeading: ", self.__heading, "\ntargetHeading: ", self.__targetHeading, "\ndeltaDirection: ", self.__deltaDirection, "\nmotor1: ", self.__motor1, "\nmotor2: ", self.__motor2, "\nclockwise: ", self.__clockwise, "\nheadingDiff: ", self.__headingDifference, "\ntime: ", int(time.time()), "\n")    
            print("------------------------------------------------")
            '''

            time.sleep(0.04)
            self.setGps()
            self.setHeading()
            self.setDistance()

        '''
        # Debug print
        print("--------------------END DATA--------------------")
        print("Destination Waypoint: ", self.__nextWaypoint, "\nCurrent GPS: ", self.__gps, "\nDistance(cm): ",self.__distance, "\nCurrent Heading: ", self.__heading)
        print("------------------------------------------------")
        '''
        if not self.__stop:
            self.notifyArrival()
