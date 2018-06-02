from socket import *
import struct
from time import sleep, time
import serial
from threading import Thread
import sys
import os
#from deepstream import get, post
#from autonomousCore import *
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

payload_size = 20 #size of payload in bytes (it's 10  x 2 byte shorts)

# LED Strip colors
ledOff = 6 # off
ghzLed = 1 # green
mhzLed = 3 # purple

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

    rf_uart.write(b's') #start byte
    rf_uart.write(data) #payload
    rf_uart.write(b'f') #end byte
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
    counter -= 1
    sleep(1)
    if counter <= 0:
        #connected = False
        #writeToBus(6, 6) # In the event we wish to turn off lights, otherwise autonomous light active
        pass

def reconnect():
    global connected
    if not connected:
        resp = os.system("ping -c 10 " + "192.168.1.8")
        if resp == 0:
            connected = True
    sleep(5) # Try to check connection again every 5 seconds - autonomous mode active during this time

def connectionLost():
    global storedPoints, connected, myDriver
    '''
    while len(storedPoints) > 0 and not connected:
        myDriver.goTo(storedPoints.pop())
    '''
    if not connected:
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
                    currentGpsLoc = (float(pointList[0]), float(pointList[1])) # IS THE SLEEP OK TO SEND BACK TO MHZ?
                    storedPoints.append(currentGpsLoc)
                except:
                    Client.close()
                    break
        sleep(5)

def sendToArduino(freq, cmd):
    try:
        unpacked = struct.unpack('10h', cmd)
        cmdList = list(map(str, unpacked))
        outString = ','.join(cmdList)
        print(outString)
        try:
            re_data = ardSocket.recvfrom(512)
            if bytes.decode(re_data[0]) == "r":
                ardSocket.sendto(bytes(outString,'utf-8'), ardConnectData)
            else:
                pass
            sleep(0.05)
        except:
            print("error writing to Arduino")
        # Write to LED lights bus
        #writeToBus(freq, int(cmdList[9]))
    except:
        print("Ard or LED error")
        pass

def stopDrv():
    global myDriver, requestStop
    if requestStop:
        myDriver.setStop()
        pass
    requestStop = False

def toggleDrvPause():
    global myDriver, toggleSuspend
    if toggleSuspend:
        myDriver.setStop()
        pass
    toggleSuspend = False

Thread(target = collectPoints).start()
Thread(target = trackConnection).start()
Thread(target = reconnect).start()
Thread(target = stopDrv).start()
Thread(target = toggleDrvPause).start()
sleep(3) # Allow thread/port initializations
ardSocket.sendto(bytes('0,0,0,0,0,0,0,0,0,0','utf-8'), ardConnectData)

while True:
    if connected:
        try:
            data = ghzSocket.recvfrom(512)[0]
            ghzSocket.sendto(bytes('xff', 'utf-8'), baseConnData)
            sendToArduino(ghzLed, data)
            '''
            try:
                re_data = ardSocket.recvfrom(512)
                print(re_data)
                if bytes.decode(re_data[0]) == "r":
                    print("got r")
                    ardSocket.sendto(bytes('0,0,0,0,0,0,0,0,0,0','utf-8'), ardConnectData)
            except:
                print("error writing to ard")
            '''
            counter = 10
        except:
            print("GHz failed - trying MHz")
            try:
                mhzData = getRF(ser, payload_size)
                sendToArduino(mhzLed, mhzData)
                #Send back current GPS
                putRF(ser, packGPS())
                counter = 10
            except:
                print("GHz, MHz failed")
