7#####################################################################################
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
#import struct
from threading import Thread
from decimal import Decimal
from deepstream import get
from leds import writeToBus

MINFORWARDSPEED = 20
MAXFORWARDSPEED = 50
TARGETTHRESHOLD = 20  # In cm
CORRECTIONTHRESHOLD = 3.5  # In degrees
HEADINGTHRESHOLD = 15 # In degrees
autoLed = 4

class Driver:

    def __init__(self):

        # Arduino address and connection information
        #self.__address = ("localhost", 5001)
        self.__address = ('192.168.1.10', 5000)
        self.__client_socket = socket(AF_INET, SOCK_DGRAM)
        self.__client_socket.settimeout(0.5)

        '''
        # Tailored to Runt Rover
        self.__angleX = [5, 15, 25]
        self.__rotateY = [40, 50, 90]
        self.__distanceX = [60, 120]
        self.__speedY = [65, 110]
        '''
        # Tailored to Rover
        self.__angleX = [5, 15, 25]
        self.__rotateY = [25, 42.5, 60]
        self.__distanceX = [20, 45]
        self.__speedY = [25, 45]

        self.__gps = (0.00, 0.00)
        self.__nextWaypoint = (0.00, 0.00)
        self.__heading = 0.0
        self.__targetHeading = 0.0
        self.__headingDifference = 0.0
        self.__clockwise = None
        self.__deltaDirection = 0.0
        self.__distance = 0.0
        self.__motor1 = 0
        self.__motor2 = 0
        self.__paused = False
        self.__stop = False
        self.__quit = False
        Thread(target = self.setStop).start()
        Thread(target = self.togglePause).start()
        Thread(target = self.quit).start()
        time.sleep(3)
        

    def calculateGps(self, origin, heading, distance):
        '''
        Description:
            Takes a GPS point, heading, and distance and calculates the next GPS point
        Args:
            Heading, Origin --> (lat, lon), and distance in cms
        Returns:
            A tuple (lat, lon)
        '''

        if type(heading) != float or type(heading) != int or type(distance) != int or type(distance) != float:
            print("Only Int or Float allowed") #raise TypeError("Only Int or Float allowed")
            #return

        if type(origin) != tuple:
            print("Only Tuples allowed") # raise TypeError("Only Tuples allowed")
            #return

        heading = math.radians(heading)
        radius = 6371 # km
        dist =  distance / 100000.0
        lat1 , lon1 = origin

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        lat2 = math.asin( math.sin(lat1)*math.cos(dist/radius) + math.cos(lat1)*math.sin(dist/radius)*math.cos(heading))
        lon2 = lon1 + math.atan2(math.sin(heading)*math.sin(dist/radius)*math.cos(lat1), math.cos(dist/radius)-math.sin(lat1)*math.sin(lat2))

        lat2 = round(math.degrees(lat2), 9)
        lon2 = round(math.degrees(lon2), 9)

        return (lat2, lon2)

    def spiralPoints(self, origin, radius):
        '''
        Description:
            Calculates a set of points located in Concentric circles in order to search the tennis ball
        Args:
            Origin --> (lat, lon), radius in Cms
        Returns:
            A list of waypoints that starts from the farthest point from the center
        '''

        if type(radius) != float or type(radius) != int:
            #raise TypeError("Only Int or Float allowed")
            #return
            print("spiralPoints break - invalid radius", radius)

        if type(origin) != tuple or type(origin[0]) != float or type(origin[0]) != int or type(origin[1]) != float or type(origin[1]) != int:
            #raise TypeError("Only Tuples allowed")
            #return
            print("not float or int")

        center = origin
        spiral = []
        if (radius / 100) % 2 != 0:
            rad = radius - 100
        else:
            rad = radius
        #print(self.calculateGps(center, 0, rad))
        while rad > 0:
            counter =  math.ceil(2 * math.pi * rad / 200)

            #print("Counter = ", counter)
            diff = round(360 / counter, 2)
            head = 0
            while counter > 0:
                point = self.calculateGps(center, head, rad)
                spiral.append(point)
                #print("AT heading ", head)
                head = round(head + diff, 2)
                counter -= 1
            rad -= 200
        return spiral

    '''
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
    '''

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
            print("Only tuples allowed") #raise TypeError("Only tuples allowed")

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
            outString = str(self.__motor1) + ',' + str(self.__motor2) + '0,0,0,0,0,0,0,4'
            self.__client_socket.sendto(bytes(outString,'utf-8'), self.__address)
            writeToBus(autoLed, autoLed)
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

    def setStop(self):
        '''
        Description:
            Used to exit the current goTo function indefinitely.
        '''
        while True:
            try:
                val = get('stop')
                if val is dict and val != {}:
                    self.__stop = val["stop"]
            except:
                print("DS stop error")

    def togglePause(self):
        '''
        Description:
            Toggles between pause state.
        '''
        while True:
            try:
                val = get('pause')
                if val is dict and val != {}:
                    self.__pause = val["pause"]
            except:
                print("DS pause error")
    
        def setQuit(self):
            '''
        Description:
            Used to quit further autonomous traversal.
        '''
        while True:
            try:
                val = get('quit')
                if val is dict and val != {}:
                    self.__quit = val["quit"]
            except:
                print("DS quit error")

    '''
    def notifyArrival(self):
        '''
        Description:
            Flashes LED pattern for on board visual cue.
        Args:
            None
        Returns:
            Nothing
        '''
        self.__motor1 = self.__motor2 = 0
        self.sendMotors()
    '''

        # Blink lights
        leds = [0, 1, 2]
        color = toggle = 0
        for i in range(12):  # Blink red, green, and blue for 3 seconds
            try:
                writeToBus(color, color)
                time.sleep(0.25)
                toggle += 1
                if toggle >= len(leds):
                    toggle = 0
                    color = leds[toggle]
            except:
                pass
                #print("led fail in notifyArrival")

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
        if type(newHeading) != float or type(newHeading) != int:
            raise TypeError("Only float/int allowed")
            #return

        self.__targetHeading = newHeading
        self.setHeading()
        self.setHeadingDifference()
        self.setDeltaDirection()
        self.setShouldTurnClockwise()
        while self.__deltaDirection > HEADINGTHRESHOLD:
            motor2 = ROTATESPEED
            if not self.__clockwise:
                motor2 = -ROTATESPEED
            motor1 = 0
            self.sendMotors()
            time.sleep(0.04)
            self.setHeading()
            self.setHeadingDifference()
            self.setDeltaDirection()
            self.setShouldTurnClockwise()

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
            print("Only tuple form allowed - exiting goTo") #raise TypeError("Only tuples allowed")
            return
        if type(point[0]) != float or type(point[0]) != int or type(point[1]) != float or type(point[1]) != int:
            print("Only float/int allowed - exiting goTo") #raise TypeError("Only floats allowed as tuple values")
            return

        self.__nextWaypoint = point
        self.setGps() 
        self.setHeading() 
        self.setDistance()

        while self.__distance > TARGETTHRESHOLD:
            self.setTargetHeading()
            self.setHeadingDifference()
            self.setDeltaDirection()
            self.setShouldTurnClockwise()
            self.calculateMotors()
            if self.__deltaDirection < CORRECTIONTHRESHOLD:
                self.__motor2 = 0
                self.__headingDifference = None
            
            if self.__stop:
                return 1
            
            if self.__quit:
                return -1

            if not self.__paused:
                self.sendMotors()
                #self.roverViewer()


                # Debug print
                '''
                print("------------------------------------------------")
                print("destWaypoint: ", self.__nextWaypoint, "\ncurrentGPS: ", self.__gps, "\ndist(cm): ", self.__distance, "\ncurrentHeading: ", self.__heading, "\ntargetHeading: ", self.__targetHeading, "\ndeltaDirection: ", self.__deltaDirection, "\nmotor1: ", self.__motor1, "\nmotor2: ", self.__motor2, "\nclockwise: ", self.__clockwise, "\nheadingDiff: ", self.__headingDifference, "\ntime: ", int(time.time()), "\n")    
                print("------------------------------------------------")
                '''

            time.sleep(0.04)
            self.setGps()
            self.setHeading()
            self.setDistance()

        # Debug print
        '''
        print("--------------------END DATA--------------------")
        print("Destination Waypoint: ", self.__nextWaypoint, "\nCurrent GPS: ", self.__gps, "\nDistance(cm): ",self.__distance, "\nCurrent Heading: ", self.__heading)
        print("------------------------------------------------")
        '''        
        
        '''
        if not self.__paused:
            self.notifyArrival()
        '''
        return 0
