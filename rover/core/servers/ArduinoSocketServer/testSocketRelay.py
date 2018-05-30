from socket import *
import struct
from time import sleep, time
import serial
from threading import Thread
import sys
import os
#from deepstream import get, post
from autonomousCore import *
from leds import writeToBus

global myDriver
global storedPoints
global cmdBuffer
global currentGpsLoc
global connected
global counter
global requestStop
global toggleSuspend
storedPoints = []
cmdBuffer = []
currentGpsLoc = (None, None) # GPS tuple (lat, lon)
counter = 10
requestStop = False
toggleSuspend = False

payload_size = 20 #size of payload in bytes 10i (10 x 2byte shorts) for full command, 2b (2 signed bytes) for mobility over mhz connection

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
except:
    print("Arduino init failed...")

# MHz initialization
try:
    ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=None)
except:
    print("Failed socketRelay MHz init")

# GHz address and connection
baseConnData = ('192.168.1.26', 5001)
ghzSocket = socket(AF_INET, SOCK_DGRAM)
ghzSocket.settimeout(0.5)
connected = True
ghzSocket.bind(('', 5002))

def packGPS():
    currGPS = struct.pack("2f", currentGpsLoc[0], currentGpsLoc[1])
    return currGPS

def putRF(rf_uart, data): #arguments to make function more self-contained and function-like
    rf_uart.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
    rf_uart.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0

    rf_uart.write(b's' + data + b'f') #start byte
    #rf_uart.write(data) #payload
    #rf_uart.write(b'f') #end byte
    rf_uart.flush() #waits until all data is written

def getRF(rf_uart, size_of_payload): #added argument to make it more function-like
    rf_uart.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
    rf_uart.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0
    while True:
        n = rf_uart.read(1) #read bytes one at a time
        if n == b's': #throw away bytes until start byte is encountered
            data = rf_uart.read(size_of_payload) #read fixed number of bytes
            n = rf_uart.read(1) #the following byte should be the stop byte
            if n == b'f':
                print('success')
                print(data)
            else: #if that last byte wasn't the stop byte then something is out of sync
                print("failure")
                return -1
    return data

def trackConnection():
    global counter, connected
    while True:
        counter -= 1
        sleep(1)
        if counter <= 0:
            connected = False
            writeToBus(6, 6) # In the event we wish to turn off lights, otherwise autonomous light active

def reconnect():
    global connected
    while True:
        if not connected:
            resp = os.system("ping -c 10 " + "192.168.1.8")
            if resp == 0:
                connected = True
        sleep(5) # Try to check connection again every 5 seconds - autonomous mode active during this time

def connectionLost():
    global storedPoints, connected, myDriver
    while True:
        while len(storedPoints) > 0 and not connected:
            myDriver.goTo(storedPoints.pop())
            writeToBus(4, 4)

def collectPoints():
    global storedPoints, connected, currentGpsLoc
    while True:
        if connected:
            host = "192.168.1.2" 
            port = 8080
            BUFFER_SIZE = 4096 

            Client = socket(AF_INET, SOCK_STREAM) 
            Client.connect((host, port))

            while True:
                try:  
                    data = Client.recv(BUFFER_SIZE)
                    pointList = data.split(',')
                    currentGpsLoc = (float(pointList[0]), float(pointList[1]))
                    storedPoints.append(currentGpsLoc)
                except:
                    Client.close()
                    break
        sleep(5)

def sendToArduino():
    global cmdBuffer
    while True:
        try:
            if cmdBuffer == []:
                #ardSocket.sendto(bytes('0,0,0,0,0,0,0,0,0,1','utf-8'), ardConnectDat$
                continue
            else:
                outString = cmdBuffer[-1]
                print(outString[0])
                ardSocket.sendto(bytes(outString[0],'utf-8'), ardConnectData)
                cmdBuffer = []

            re_data = ardSocket.recvfrom(512)
            while bytes.decode(re_data[0]) != "r":
                re_data = ardSocket.recvfrom(512)
            '''
            if cmdBuffer == []:
                ardSocket.sendto(bytes('0,0,0,0,0,0,0,0,0,1','utf-8'), ardConnectData)
                continue
            else:
                outString = cmdBuffer[-1]
                print(outString[0])
                ardSocket.sendto(bytes(outString[0],'utf-8'), ardConnectData)
                cmdBuffer = []
            '''
            try:
                # Write to LED lights bus
                writeToBus(int(outString[0][-1]), int(outString[1]))
            except:
                print("LED error")
        except:
            print("Ard fail")
            pass

def stopDrv():
    global myDriver, requestStop
    while True:
        if requestStop:
            myDriver.setStop()
            pass
        requestStop = False

def toggleDrvPause():
    global myDriver, toggleSuspend
    while True:
        if toggleSuspend:
            myDriver.setStop()
            pass
        toggleSuspend = False

def storeCmd(cmd, freq):
    global cmdBuffer
    unpacked = struct.unpack('10h', cmd)
    cmdList = list(map(str, unpacked))
    cmdBuffer.append((','.join(cmdList), freq))

#Thread(target = collectPoints).start()
#Thread(target = trackConnection).start()
#Thread(target = reconnect).start()
#Thread(target = stopDrv).start()
#Thread(target = toggleDrvPause).start()
#sleep(3) # Allow thread/port initializations
ardSocket.sendto(bytes('0,0,0,0,0,0,0,0,0,0','utf-8'), ardConnectData)
Thread(target=sendToArduino).start()
try:
    while True:
        if connected:
            try:
                data = ghzSocket.recvfrom(512)[0]
                ghzSocket.sendto(bytes('xff', 'utf-8'), baseConnData)
                storeCmd(data, ghzLed)
                counter = 10
            except:
                print("GHz failed - trying MHz")
                try:
                    mhzData = getRF(ser, payload_size)
                    print(mhzData)
                    storeCmd(mhzData, mhzLed)
                    counter = 10
                    try:
                        #Send back current GPS
                        putRF(ser, packGPS())
                    except:
                        print("put rf failed")
                except:
                    print("failed mhz")
except:
    print("Keyboard Interrupt")
    ghzSocket.close()
