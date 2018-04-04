#!/usr/bin/env python3.5
import socket
import serial
from time import time, sleep
localAddress = "0.0.0.0" # bind to local address
port = 9005 #listening port
oDevice = "/dev/ttyUSB0" #hc12 device used for output to rover
baudRate = 1200
oSerial = serial.Serial(oDevice, baudRate, timeout=None)
iSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TIMEOUT = 5 #timeout in seconds 
buf = bytearray(100)
try:
    iSock.bind((localAddress, port))
    print("binding")
except:
    print("Failed to bind!")
try:
    iSock.listen(5)
    print("listening")
except:
    print("failed to listen?")
try:
    rSock, iAddress = iSock.accept() #socket to return address, address of connection
    print("accepted socket")
except:
     print("Failed to accept connection!")   

try:
    while True:
        try:
            print("receiving")
            buf = rSock.recv(100)
            print (len(buf))
            if (len(buf) > 1):
                last_receive_time = time()
                print("last receive time")
                print(last_receive_time)
            else:
                current_time = time()
                inactivity_duration = current_time - last_receive_time
                print("inactivity")
                print(inactivity_duration)
                if inactivity_duration > TIMEOUT:
                    print("rose timeout")
                    raise TimeoutError('TIMEOUT')
                
            sleep(1)
        except:
            print('TIMED OUT\n reopening socket')
            rSock.close()
            iSock.close()
            print("sleeping")
            sleep(1)
            try:
                iSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                print("remake isock")
            except:
                print("couldn't remake isock")
            try:
                iSock.bind((localAddress, port))
                print("binding")
            except:
                print("Failed to bind!")
            try:
                iSock.listen(5)
                print("listening")
            except:
                print("failed to listen?")
            try:
                rSock, iAddress = iSock.accept() #socket to return address, address of connection
                print("accepted socket")
            except:
                print("Failed to accept connection!")  
            continue

        try:
            print("writing")
            oSerial.write(buf)
            sleep(1)
        except:
            print("Failed to write.")
except:
    print("Connection interuppted!")
    rSock.close()
    iSock.close()
    print("Sockets closed.")
