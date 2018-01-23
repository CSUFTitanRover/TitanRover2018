from threading import Thread
from socket import *
from deepstream import get, post
from time import sleep
import time
import serial
import math
from subprocess import Popen, PIPE
from kml import addPoint, saveKML
import subprocess

#   Connection to the Rover Arduino

address = ("192.168.1.10", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

#   Defining Global variables

global reach, imu, points
reach = {}
imu = {}
points = []

global lat1, lat2, lon1, lon2, heading, currLat, currLon
lat1 = 0
lon1 = 0
lat2 = 0
lon2 = 0
currLat = 0
currLon = 0
heading = 0
timeDiff = 0
thread = True

global mode, mobilityTime, previousMobilityTime
mode = "manual"                     #The Initial mode is always manual
mobilityTime = None
if get('mobilityTime') != "NO_RECORD":
    previousMobilityTime = get('mobilityTime')["mobilityTime"]
else:
    previousMobilityTime = None


device = "/dev/arduinoReset"
baud = 4800
err = "0"

#   This loop synchronizes the clocks between the RoverPi and the BasePi

while err != "":
    sleep(3)
    out, err = Popen(["ssh", "root@192.168.1.3", "date +%s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode()
    print("OUT:", out)
    print("ERR:", err)
    if out != "":
        date = out[:-1]
        Popen(["date", "-s", "@" + str(date)])
    sleep(3)

#   Function to get mobilityTime Stamp, heading from imu, gps coordinates from deepstream

def getDataFromDeepstream():
    global reach, imu, mobilityTime, heading, thread, timeDiff
    print("getting in getDataFromDeepstream")
    sleep(0.3)
    
    while mobilityTime == None or mobilityTime == "NO_RECORD" or mobilityTime == previousMobilityTime:
        try:
            mobilityTime = get('mobilityTime')["mobilityTime"]          #   Initializing the mobilityTime from deepstream
        except:
            print("Still Getting the initial Mobility Time")
        
        sleep(0.05)
        
        print("Initial Mobility Time : ", mobilityTime)
        sleep(0.5)
    
    t2.start()
    
    while thread:
        try:
            try:
                print("getting GPS")
                reach = get("gps")              #   getting the entire GPS data object(json)
                if type(reach) == dict:
                    print("passing to function storedataindeepstream")
                    if reach != {}:
                        storeDataInList(reach)
                #lat = reach['lat']
                #lon = reach['lon']
            except:
                reach = "NO_RECORD"
                #print("reach : ", reach)
            #print("Latitude : " + str(lat) + "   Longitude : " + str(lon))
            sleep(.025)
            
            try:
                print("Getting IMU")
                imu = get("imu")
                heading = imu['heading']        #   getting the current heading (with respect to true North) from deepstream
                #print(heading)
            except:
                imu = {}
                print("imu : ", imu)
            sleep(.025)
           
            try:
                print("Getting Mobility time stamp")
                mobilityTime = get('mobilityTime')["mobilityTime"]      #   periodically getting the mobilityTime to compare and switch modes 
                print("Current Mobility Time : ", mobilityTime)
            except:
                print("Mobility Time : ", mobilityTime)
                sleep(0.3)
                pass
            
            try:
                post({"timeDiff": str(timeDiff)}, "timeDiff")
            except:
                pass
                
            #print("Latitude : " + str(lat) + "    Longitude : " + str(lon) + "    heading : " + str(heading) + "    MobilityTime : " + mobilityTime)
            sleep(.025)
            
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            saveKML()
            thread = False
            sleep(3)
            try:
                post({"mode":"manual"}, mode)
            except:
                print("There was a problem setting mode back to manual")

#   Function to check mobilityTime and switch modes between manual and autonomanual

def switchToAutonomanual():
    global mobilityTime, mode, thread, timeDiff
    print("getting in switchToAutonomaual")
    while thread:
        sleep(.3)
        #print("mobility time : ", mobilityTime)
        if(type(mobilityTime) == int):
            timeDiff = (mobilityTime - time.time())
            #print("\nThe Time Difference is : ", (mobilityTime - time.time()))
            if mobilityTime + 10 < int(time.time()) or mode == "autonomanual":
                print("checking for autonomanual mode")        
                if mode != "autonomanual":
                    try:
                        print("changing mode to autonomanual and posting to deepstream")
                        #ser = serial.Serial(device, baud, timeout = 0.5)
                        #ser.write("1")
                        sleep(8)
                        mode = "autonomanual"
                    except:
                        print("Error In changing modes to Autonomanual so setting mode to MANUAL")
                        mode = "manual"
                    print("The Current Mode is : ", mode)
                    post({"mode" : mode}, "mode")
                    sleep(2)
                    print("SENDING DATA TO ARDUINO TO STOP")
                    print("0,0,0,0,0,0,0,0,0,1")
                    #client_socket.sendto(bytes("0,0,0,0,0,0,0,0,0,1", "utf-8"), address)
                elif int(mobilityTime) + 10 > int(time.time()):
                    print("Entering Into MANUAL MODE Again")
                    mode = "manual"
                    post({"mode" : mode}, "mode")
                    print("The Current Mode is : ", mode)
                    sleep(2)
                else:
                    try:
                        re_data = client_socket.recvfrom(512)
                        if bytes.decode(re_data[0]) == "r":
                            #print("SENDING DATA TO ARDUINO TO TAKE REVERSE")
                            #print("-20,0,0,0,0,0,0,0,0,4")
                            #client_socket.sendto(bytes("-20,0,0,0,0,0,0,0,0,4","utf-8"), address)
                            returnToStart()
                        sleep(.05)
                    except:
                        print("Send failed")
                
#   Function to store 350 gps coordinates to travele back to the starting point

def storeDataInList(reach):
    print("Getting into storeDataInList")
    global lat1, lat2, lon1, lon2, points, reach
    lat2, lon2 = reach['lat'], reach['lon']

    # PUT KML data here
    if lat1 != 0 and lon1 != 0:
        addPoint(lat1, lon1)

    if distance((lat1, lon1), (lat2, lon2)) > 3 and reach['sde'] < 10 and reach['sdn'] < 10 and reach['fix'] and mode == "manual":
        if len(points) < 350:
            points.append((lat2, lon2))
        else: 
            del points[0]
            points.append((lat2, lon2))
            #print("Latitude and Longitude")
    
    lat1 = lat2
    lon1 = lon2
    
    print("Recorded Points : ", points)
    sleep(1)

#   Haversine formula to calculate distance between two gps coordinates

def distance(origin, destination):
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

#   Function to get angle between tw0 GPS coordinates with respect to true North

def reverseGpsDirection(origin, destination):      #Always clockwise Direction turn Angle
    print("Getting into reverseGpsDirection")
    a1, b1 = origin                                #First Coordinate
    a2, b2 = destination                           #Second Coordinate

    dlon = b2 - b1

    y = math.sin(dlon) * math.cos(a2)
    x = math.cos(a1) * math.sin(a2) - math.sin(a1) * math.cos(a2) * math.cos(dlon)

    revDir = math.atan2(y, x)

    revDir = math.degrees(revDir)
    #revDir = (math.degrees(revDir) + 180) % 360   # This is clockwise
    #print(revDir)
    #revDir = (math.degrees(revDir) + 360) % 360   # This is Anti-clockwise
    #print(revDir)
    return revDir


def revDir(heading):
    #print("Getting into revDir")
    return (heading + 180) % 360 


def returnToStart():
    global heading, points, currLat, currlon
    '''
    print("#### TAKING A 180 DEGREE TURN ####")
    sleep(0.5)
    revTurn = revDir(heading)
    while heading not in range(revTurn-.5, revTurn+.5):
        try:
            re_data = client_socket.recvfrom(512)
            if bytes.decode(re_data[0]) == "r":
                #print("SENDING DATA TO ARDUINO TO TAKE REVERSE")
                #print("-30,30,0,0,0,0,0,0,0,4")
                client_socket.sendto(bytes(",-30,30,0,0,0,0,0,0,4","utf-8"), address)
                sleep(.05)
        except:
            print("Send failed")
            sleep(.1)
    '''
    print("#### RETURNING BACK TO THE STARTING POINT ####")
    while len(points) > 1:
        try:
            if type(reach) == dict:
                if reach != {}:
                    currLat, currLon = reach['lat'], reach['lon']
            else:
                continue

            angle = reverseGpsDirection(points[-1], points[-2])
            if angle < 0:
                print("Taking a RIGHT TURN (CLOCKWISE)")
                sleep(0.05)
                while heading not in range(abs(angle) - 0.5, abs(angle) + 0.5):
                    try:
                        re_data = client_socket.recvfrom(512)
                        if bytes.decode(re_data[0]) == "r":
                            client_socket.sendto(bytes("-30,30,0,0,0,0,0,0,0,4","utf-8"), address)
                            sleep(.05)
                    except:
                        print("Send failed")
                        sleep(.1)

            elif angle > 0:
                print("Taking a LEFT TURN (ANTI - CLOCKWISE)")
                sleep(0.05)
                while heading not in (360 - range(angle - 0.5, angle + 0.5)):
                    try:
                        re_data = client_socket.recvfrom(512)
                        if bytes.decode(re_data[0]) == "r":
                            client_socket.sendto(bytes("-30,30,0,0,0,0,0,0,0,4","utf-8"), address)
                            sleep(.05)
                    except:
                        print("Send failed")
                        sleep(.1)

            elif angle == -0:
                print("Taking a 180 DEGREE TURN")
                sleep(0.05)
                while heading not in range(179.50, 180.50):
                    try:
                        re_data = client_socket.recvfrom(512)
                        if bytes.decode(re_data[0]) == "r":
                            client_socket.sendto(bytes("-30,30,0,0,0,0,0,0,0,4","utf-8"), address)
                            sleep(.05)
                    except:
                        print("Send failed")
                        sleep(.1)

            while distance(points[-1], (currLat, currLon)) > 0.5:
                try:
                    currLat, currLon = reach['lat'], reach['lon']
                    re_data = client_socket.recvfrom(512)
                    if bytes.decode(re_data[0]) == "r":
                        print("SENDING DATA TO ARDUINO TO GO BACK AT START POINT")
                        client_socket.sendto(bytes("20,20,0,0,0,0,0,0,0,4", "utf-8"), address)
                        sleep(.05)
                except:
                    print("Send failed")
                    sleep(.1)
            points.pop()
        except:
            print("#### ERROR GOING BACK ####")
            sleep(0.1)


print("Starting The Threads")

t1 = Thread(target=getDataFromDeepstream)
t2 = Thread(target=switchToAutonomanual)

t1.start()
sleep(5)