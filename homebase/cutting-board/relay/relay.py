#!/usr/bin/env python3.5
import socket
import serial
from time import time, sleep
localAddress = "0.0.0.0" # bind to local address
port = 9005 #listening port
oDevice = "/dev/ttyUSB0" #hc12 device used for output to rover
baudRate = 9600
TIMEOUT = 1 #timeout in seconds 
buf = bytearray(1024)

def initRF(oDevice, baudRate):
    while True:#try to initialize device until it works
        try:
            oSerial = serial.Serial(oDevice, baudRate, timeout=None) #no timeout on uart rf module
            print("Device assigned")
            return oSerial
        except:
            print("Check connection to rf module")
            sleep(1)
            continue

def initSocket(localAddress, port):
    while True: #used like a label, if an initialization fails retry all
        try:
            print("initializing socket")
            iSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("couldn't initialize")
            sleep(1)
            continue
        try:
            print("binding")
            iSock.bind((localAddress, port))
        except:
            print("Failed to bind!")
            sleep(1)
            continue
        try:
            iSock.listen(5)
            print("listening")
        except:
            print("failed to listen?")
            sleep(1)
            continue
        try:
            rSock, iAddress = iSock.accept() #socket to return address, address of connection
            print("accepted socket")
        except:
            print("Failed to accept connection!")  
            sleep(1)
            continue 
        return iSock, rSock#if everything works then don't retry anything

#receive from socket, send over uart to rf module
print("calling RF function")
oSerial = initRF(oDevice, baudRate)     #initialize rf and socket the first time no matter what
print("calling socket function")
iSock, rSock = initSocket(localAddress, port)

oSerial.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
oSerial.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0
oSerial.open() #applies dtr and rts pins


while True:
    try:
        print("receiving")
        buf = rSock.recv(1024)
        print (len(buf))#prints number of bytes received
        if (len(buf) > 1):#if it received something update the time of last received data
            last_receive_time = time()
            #print("last receive time")
            #print(last_receive_time)
        else:#if nothing was received check how long it was since the last reception and raise a timeout if appropriate
            current_time = time()
            inactivity_duration = current_time - last_receive_time
            print("inactivity")
            print(inactivity_duration)
            if inactivity_duration > TIMEOUT:
                print("rose timeout")
                raise TimeoutError('TIMEOUT')
    except:
        print('TIMED OUT\n reopening socket')
        rSock.close()#closed for good measure but this socket is never used so it doesn't matter
        iSock.close()
        iSock, rSock = initSocket(localAddress, port)
        continue
    try:
        print("writing")
        oSerial.write(buf)
    except:
        print("Failed to write.")
        oSerial.close()
        oSerial = initRF(oDevice, baudRate)

