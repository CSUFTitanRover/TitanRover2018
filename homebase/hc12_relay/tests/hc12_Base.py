#!/usr/bin/env python
import socket
from time import sleep
import sys

print("initializing")
oAddress = "192.168.1.5" #sends data out to this ip address
oPort = 9005 #listening port
oSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

while(True):
    
    try:
        print("connecting")
        oSock.connect((oAddress, oPort))
    except:
        print("Failed to connect!")
	sleep(1)
        continue
	#sys.exit()
    try:
        while True:
            print("sending")
            oSock.send(bytearray('Hello World', 'utf-8'))
            sleep(1)
    except:
        print("Connection Interupted!")
        oSock.close()
        print("Socket Closed.")
