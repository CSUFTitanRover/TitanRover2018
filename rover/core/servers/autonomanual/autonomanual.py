from threading import Thread
from socket import *
from deepstream import get, post
from time import sleep
import time
import serial
import math
from subprocess import Popen, PIPE
from kml import addPoint, saveKML

address = ("192.168.1.10", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

global reach, imu, points
reach = {}
imu = {}
points = []

global lat1, lat2, lon1, lon2, heading, counter
lat1 = 0
lon1 = 0
lat2 = 0
lon2 = 0
heading = 0
counter = 0

global mode, mobilityTime
mode = "manual"
mobilityTime = None


device = "/dev/arduinoReset"
baud = 4800
err = "0"

while err != '':
    sleep(3)
    out, err = Popen(["ssh", "root@192.168.1.3", "date +%s"], stdout=PIPE, stderr=PIPE).communicate()
    print(err)
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    print("OUT:", out)
    print("ERR:", err)
    if out != "":
        date = out[:-1]
        Popen(["date", "-s", "@" + str(date) + ""]).communicate()
    sleep(3)
    if err == "channel 0: open failed: administratively prohibited: open failed\r\n":
        break


def getDataFromDeepstream():
    global reach, imu, mobilityTime, heading
    #print("getting in getDataFromDeepstream")
    sleep(1)
    
    while mobilityTime == None or mobilityTime == "NO_RECORD":
        try:
            mobilityTime = get('mobilityTime')["mobilityTime"]
        except:
            pass
        sleep(1)
    
    while True:
        try:
            try:
                #print("getting GPS")
                reach = get("gps")
                if type(reach) == dict:
                    #print("passing to function storedataindeepstream")
                    sleep(1)
                    if reach != {}:
                        storeDataInList(reach)
                #lat = reach['lat']
                #lon = reach['lon']
            except:
                reach = "NO_RECORD"
            #print("Latitude : " + str(lat) + "   Longitude : " + str(lon))
            sleep(.025)
            
            try:
                #print("Getting IMU")
                imu = get("imu")
                heading = imu['heading']
                #print(heading)
            except:
                imu = {}
            sleep(.025)
           
            try:
                print("Getting Mobility time stamp")
                mobilityTime = get('mobilityTime')["mobilityTime"]
            except:
                pass
            #print("Latitude : " + str(lat) + "    Longitude : " + str(lon) + "    heading : " + str(heading) + "    MobilityTime : " + mobilityTime)
            sleep(.025)
            
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            saveKML()



def switchToAutonomanual():
    global mobilityTime, mode
    #print("getting in switchToAutonomaual")
    while True:
        if(type(mobilityTime) == int):
            if int(mobilityTime) + 10 < time.time() or mode == "autonomanual":        
                if mode != "autonomanual":
                    try:
                        ser = serial.Serial(device, baud, timeout = 0.5)
                        ser.write("1")
                        mode = "autonomanual"
                    except:
                        mode = "manual"
                    post({"mode" : "autonomanual"}, "mode")
                    sleep(4)
                    client_socket.sendto(bytes("0,0,0,0,0,0,0,0,0,1", "utf-8"), address)
                else:
                    try:
                        re_data = client_socket.recvfrom(512)
                        if bytes.decode(re_data[0]) == "r":
                            client_socket.sendto(bytes("20,-20,0,0,0,0,0,0,0,3","utf-8"), address)
                        sleep(.05)
                    except:
                        print("Send failed")

def storeDataInList(reach):
    #print("Getting into storeDataInList")
    global counter, lat1, lat2, lon1, lon2, points
    lat2, lon2 = reach['lat'], reach['lon']

    # PUT KML data here
    addPoint(lon1, lon1)

    if distance((lat1, lon1), (lat2, lon2)) > 3 and reach['sde'] < 10 and reach['sdn'] < 10 and reach['fix']:
        if counter < 350:
            points.append((lat2, lon2))
            counter += 1
        else: 
            del points[0]
            points.append((lat2, lon2))
            print("Latitude and Longitude")
    
    lat1 = lat2
    lon1 = lon2
    
    sleep(1)
    print(points)
    sleep(1)



def distance(origin, destination):
    #print("getting into Distance")
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

def reverseGpsDirection(origin, destination):      #Always clockwise Direction turn
    #print("Getting into reverseGpsDirection")
    a1, b1 = origin
    a2, b2 = destination

    dlon = b2 - b1

    y = math.sin(dlon) * math.cos(a2)
    x = math.cos(a1) * math.sin(a2) - math.sin(a1) * math.cos(a2) * math.cos(dlon)

    revDir = math.atan2(y, x)

    revDir = (math.degrees(revDir) + 180) % 360   # This is clockwise
    #print(revDir)
    #revDir = (math.degrees(revDir) + 360) % 360   # This is Anti-clockwise
    #print(revDir)
    return revDir


def revDir(heading):
    #print("Getting into revDir")
    return (heading + 180) % 360 

#print("Starting The Threads")

t1 = Thread(target = getDataFromDeepstream)
t2 = Thread(target = switchToAutonomanual)

t1.start()
t2.start()
