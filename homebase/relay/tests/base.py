#!/usr/bin/env python
#simulates the base station sending data over socket
import socket
from time import sleep
import sys

print("initializing")
oAddress = "192.168.1.42" #sends data out to this ip address
oPort = 9005 #listening port

while(True):
    
    try:
        print("Initializing socket")
        oSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #this needs to be re-called in a loop when attempting to reconnect
    except:
        print("failed to initialize socket.")
        sleep(0.5)
        continue
    try:
        print("connecting")
        oSock.connect((oAddress, oPort))
    except:
        print("Failed to connect!")
        sleep(0.5)
        continue
    try:
        while True:
            print("sending")
            oSock.send(bytearray(0xFFFFFFFFFFFFFFFF))
            sleep(0.5)
            #oSock.send(bytearray('World!', 'utf-8'))
            #sleep(0.5)

    except:
        print("Connection Interupted!")
        oSock.close()
        print("Socket Closed.")
        continue
