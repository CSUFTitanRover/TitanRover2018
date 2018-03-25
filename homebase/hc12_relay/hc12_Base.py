#!/usr/bin/env python
import socket
from time import sleep
print("initializing")
oAddress = "192.168.1.179" #sends data out this ip address
oPort = 9005 #listening port
oSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

try:
    oSock.connect((oAddress, oPort))
    print("connecting")
except:
    print("Failed to connect!")

try:
    while True:
        print("sending")
        oSock.send(bytearray('Hello World', 'utf-8'))
        sleep(1)
except:
    print("Connection Interupted!")
    oSock.close()
    print("Socket Closed.")
