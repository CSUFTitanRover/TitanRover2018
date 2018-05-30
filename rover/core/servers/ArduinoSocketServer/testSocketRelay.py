from socket import *
import struct
from time import sleep, time
import serial
import subprocess
from threading import Thread
import sys
import os
from deepstream import get
from autonomousCore import *
from leds import writeToBus

global myDriver
global storedPoints
global cmdBuffer
global currentGpsLoc
global ghzConnection
global mhzConnection
global ghzCountdown
global mhzCountdown
global countdown
global requestStop
global toggleSuspend
storedPoints = []
cmdBuffer = []
currentGpsLoc = (0.00, 0.00) # GPS tuple (lat, lon)
countdown = 10
ghzCountdown = 5
mhzCountdown = 5
requestStop = False
toggleSuspend = False
ghzConnection = False
mhzConnection = False

payload_size = 20 #size of payload in bytes 10i (10 x 2byte shorts) for full command, 2b (2 signed bytes) for mobility over mhz connection

# LED Strip colors
ledOff = 6 # off
ghzLed = 1 # green
mhzLed = 3 # purple
drivingMode = 2 # blue

# Autonomous module object
#myDriver = Driver()

# Arduino address and connection
try:
    ardConnectData = ('192.168.1.10', 5000)
    ardSocket = socket(AF_INET, SOCK_DGRAM)
    ardSocket.settimeout(0.5)
except:
    print("Arduino init failed...")

# MHz initialization
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
    mhzConnection = True
except:
    print("Failed socketRelay MHz init")

# GHz address and connection
baseConnData = ('192.168.1.121', 5001) # 192.168.1.8 for base station
ghzSocket = socket(AF_INET, SOCK_DGRAM)
ghzSocket.settimeout(0.5)
ghzConnection = True
ghzSocket.bind(('', 5002))

def packGPS():
    global currentGpsLoc
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
    n = rf_uart.read(1) #read bytes one at a time
    while True:
        if n == b's': #throw away bytes until start byte is encountered
            data = rf_uart.read(size_of_payload) #read fixed number of bytes
            n = rf_uart.read(1) #the following byte should be the stop byte
            if n == b'f':
                #print(data)
                return data
            else: #if that last byte wasn't the stop byte then something is out of sync
                print("return bytes successful")
                return -1

def trackGhzConnection():
    global ghzCountdown, ghzConnection
    while True:
        if ghzConnection:
            ghzCountdown -= 1
            if ghzCountdown <= 0:
                ghzConnection = False
        sleep(1)

def reconnect():
    global ghzConnection
    while True:
        if not ghzConnection:
            resp = os.system("ping -c 10 " + "192.168.1.8")
            if resp == 0:
                ghzConnection = True
        sleep(5) # Try to check connection again every 5 seconds - autonomous mode active during this time

def connectionLost():
    global storedPoints, ghzConnection, mhzConnection, myDriver
    while True:
        while len(storedPoints) > 0 and not ghzConnection and not mhzConnection:
            myDriver.goTo(storedPoints.pop())
            writeToBus(4, 4)
        

def dist(origin, dest):
    a1, b1 = origin
    a2, b2 = dest
    radius = 6371 # km

    da = math.radians(a2-a1)
    db = math.radians(b2-b1)
    a = math.sin(da/2) * math.sin(da/2) + math.cos(math.radians(a1)) \
        * math.cos(math.radians(a2)) * math.sin(db/2) * math.sin(db/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d * 100000

def collectPoints():
    global storedPoints, ghzConnection, currentGpsLoc
    prevPoint = (0.00, 0.00)
    while True:
        if ghzConnection:
            gps = get('gps')
            currentGpsLoc = (gps['lat'], gps['lon']) 
            if dist(prevPoint, currentGpsLoc) > 500:    
                storedPoints.append(currentGpsLoc)
                prevPoint = currentGpsLoc
        sleep(5)

def sendToArduino():
    global cmdBuffer
    while True:
        try:
            if cmdBuffer == []:
                continue
            else:
                outString = cmdBuffer[-1]
                print(outString[0])
                if outString[1] == ghzLed:
                    ardSocket.sendto(bytes(outString[0][:-2],'utf-8'), ardConnectData)
                elif outString[1] == mhzLed:
                    #for i in range(2):
                    ardSocket.sendto(bytes(outString[0], 'utf-8'), ardConnectData)
                cmdBuffer = []

            re_data = ardSocket.recvfrom(512)
            while bytes.decode(re_data[0]) != "r":
                re_data = ardSocket.recvfrom(512)
            #print("after reading r: ", re_data)

            try:
                # Write to LED lights bus
                writeToBus(int(outString[0][-1]), ghzLed) if int(outString[1]) == ghzLed else writeToBus(drivingMode, mhzLed)
            except:
                print("LED error")
        except:
            cmdBuffer = []
            #print("Ard fail")
            pass

def stopDrv():
    global myDriver, requestStop
    while True:
        try:
            stopRecord = get("stop")
        except:
            print("stopDrv: DS get failed")
            continue
        if stopRecord == True:
            myDriver.setStop()
            requestStop = False

def toggleDrvPause():
    global myDriver, toggleSuspend
    while True:
        try:
            pauseRecord = get("pause")
        except:
            print("toggleDrvPause: DS get failed")
            continue
        if not pauseRecord == toggleSuspend:
            myDriver.setPause()
            toggleSuspend = not toggleSuspend

def storeCmd(cmd, freq):
    global cmdBuffer
    if freq == 1:
        unpacked = struct.unpack('9h', cmd)
    else:
        unpacked = struct.unpack('2b', cmd)
    cmdList = list(map(str, unpacked))
    cmdBuffer.append((','.join(cmdList), freq))

def readMhz():
    global storedPoints, mhzConnection, ghzConnection, mhzCountdown
    while True:
        if not ghzConnection:
            try:
                mhzData = getRF(ser, 2)
                #print(mhzData)
                if mhzData == -1:
                    continue
                storeCmd(mhzData, mhzLed)
                mhzCountdown = 10
                try:
                    #Send back current GPS
                    putRF(ser, packGPS())
                except:
                    print("put rf failed")
            except:
                print("failed mhz")

Thread(target = collectPoints).start()
Thread(target = trackGhzConnection).start()
Thread(target = reconnect).start()
Thread(target = stopDrv).start()
Thread(target = toggleDrvPause).start()
Thread(target = readMhz).start()
Thread(target = connectionLost),start()
sleep(3) # Allow thread/port initializations
ardSocket.sendto(bytes('0,0,0,0,0,0,0,0','utf-8'), ardConnectData)
Thread(target=sendToArduino).start()


while True:
    if ghzConnection:
        try:
            data = ghzSocket.recvfrom(512)[0]
            ghzSocket.sendto(bytes('xff', 'utf-8'), baseConnData)
            storeCmd(data, ghzLed)
            ghzCountdown = 10
        except (KeyboardInterrupt, SystemExit):
            ghzSocket.close()
            raise
        except:
            print("GHz failed - trying MHz")
            pass
