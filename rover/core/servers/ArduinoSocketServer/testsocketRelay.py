import socket
import struct
from time import sleep, time
import serial
from threading import Thread
import sys
import os
from autonomousCore import *
from leds import writeToBus

global myDriver
global storedPoints
global currentGpsLoc
global connected
global counter
global requestStop
global toggleSuspend
storedPoints = []
currentGpsLoc = (None, None) # GPS tuple (lat, lon)
counter = 10
requestStop = False
toggleSuspend = False

# LED Strip colors
ledOff = 6 # off
ghzLed = 1 # green
mhzLed = 3 # purple

# Autonomous module object
myDriver = Driver()

# Arduino address and connection
try:
    ardConnectData = ('192.168.1.10', 5000)
    ardSocket = socket(AF_INET, SOCK_DGRAM)
    ardSocket.settimeout(0.5)
    ardSocket.sendto('0,0,0,0,0,0,0,0,0,0', ardConnectData)
except:
    print("Arduino init failed...")

# MHz initialization
ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=None)

# GHz address and connection
tx2ConnData = ('192.168.1.2', 5001)
ghzSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ghzSocket.settimeout(0.5)
connected = True

'''
# GHz localhost address and connection
localConnData = ('', 5001)
localConnectData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localConnectData.settimeout(0.5)
'''

def trackConnection():
    global counter, connected
    counter -= 1
    sleep(1)
    if counter <= 0:
        connected = False
        #writeToBus(6, 6) # In the event we wish to turn off lights, otherwise autonomous light active

def reconnect():
    global connected
    if not connected:
        resp = os.system("ping -c 10 " + "192.168.1.8")
        if resp == 0:
            connected = True
    sleep(5) # Try to check connection again every 5 seconds - autonomous mode active during this time

def connectionLost():
    global storedPoints, connected, myDriver
    while len(storedPoints) > 0 and not connected:
        myDriver.goTo(storedPoints.pop())

def collectPoints():
    global storedPoints, connected, currentGpsLoc
    while True:
        if connected:
            host = "192.168.1.2" 
            port = 8080
            BUFFER_SIZE = 4096 

            Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            Client.connect((host, port))

            while True:
                try:  
                    data = Client.recv(BUFFER_SIZE)
                    pointList = data.split(',')
                    currentGpsLoc = (float(pointList[0]), float(pointList[1])) # IS THE SLEEP OK TO SEND BACK TO MHZ?
                    storedPoints.append(currentGpsLoc)
                except:
                    Client.close()
                    break
        sleep(5)

def sendToArduino(cmd, freq):
    try:
        # Write to Arduino socket
        unpacked = struct.unpack('10h', cmd)
        cmdList = list(map(str, unpacked))
        outString = ','.join(cmdList)
        sockArd.sendto(bytes(outString,'utf-8'), arduino_address)
        # Write to LED lights bus
        writeToBus(freq, int(cmdList[9]))
    except:
        print("Could not make initial connection to the arduino...")
        pass

def stopDrv():
    global myDriver, requestStop
    if requestStop:
        myDriver.setStop()
    requestStop = False

def toggleDrvPause():
    global myDriver, toggleSuspend
    if toggleSuspend:
        myDriver.setStop()
    toggleSuspend = False

Thread(target = collectPoints).start()
Thread(target = trackConnection).start()
Thread(target = reconnect).start()
Thread(target = stopDrv).start()
Thread(target = toggleDrvPause).start()
sleep(3) # Allow thread/port initializations

while True:
    if connected:
        try:
            data = ghzSocket.recvfrom(512)[0]
            #sleep(0.25)
            #print("data received from tx2")
            ghzSocket.sendto('xff', tx2ConnData)
            #print("send to tx2 completed")
            sendToArduino(ghzLed, cmd)
            counter = 10
        except:
            #print("failed to receive ghz")
            try:
                print("To add Georden MHz receive")
                mhzData = ser.read_all() # receive MHz from Georden
                sendToArduino(mhzLed, cmd)
                #Send back current GPS
                counter = 10
            except:
                print("GHz, MHz failed")