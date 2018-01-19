from threading import Thread
from socket import *
from deepstream import get, post
from time import sleep
import time
import serial 

address = ("192.168.1.10", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

global reach, imu, lat, lon, heading, mobilityTime, mode
lat = 0
lon = 0
heading = 0
reach = {}
imu = {}
mobilityTime = None
mode = "manual"

device = "/dev/arduinoReset"
baud = 4800


def getDataFromDeepstream():
    global reach, imu, mobilityTime
    while mobilityTime == None or mobilityTime == "NO_RECORD":
        try:
            mobilityTime = get('mobilityTime')["mobilityTime"]
        except:
            pass
        sleep(1)

    while True:
        '''
        try:
            reach = get("gps")
            lat = reach['lat']
            lon = reach['lon']
        except:
            reach = "NO_RECORD"
        #print("Latitude : " + str(lat) + "              Longitude : " + str(lon))
        sleep(.08)
        try:
            imu = get("imu")
            heading = imu['heading']
        except:
            imu = {}
        '''
        try:
            mobilityTime = get('mobilityTime')["mobilityTime"]
        except:
            pass
        #print("Latitude : " + str(lat) + "    Longitude : " + str(lon) + "    heading : " + str(heading) + "    MobilityTime : " + mobilityTime)
        sleep(.08)


def switchToAutonomanual():
    global mobilityTime, mode
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
                            client_socket.sendto(bytes("5,5,0,0,0,0,0,0,0,3","utf-8"), address)
                    except:
                        print("Send failed")



t1 = Thread(target = getDataFromDeepstream)
t2 = Thread(target = switchToAutonomanual)

t1.start()
t2.start()