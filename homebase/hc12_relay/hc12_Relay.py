#!/usr/bin/env python3.5
import socket
import serial
from time import sleep

localAddress = "0.0.0.0" # bind to local address
port = 9005 #listening port
oDevice = "/dev/ttyUSB0" #hc12 device used for output to rover
baudRate = 1200
oSerial = serial.Serial(oDevice, baudRate, timeout=None)
iSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
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
            buf = rSock.recv(100)
            print("receiving")
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
        print("writing")
        oSerial.write(buf)
        sleep(1)
except:
    print("Connection interuppted!")
    rSock.close()
    iSock.close()
    print("Sockets closed.")
