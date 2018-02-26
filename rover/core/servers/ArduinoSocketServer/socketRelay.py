"""
    Richard Stanley
    TitanRover 2018
    The purpose of this code is to hold a socket connection out 3.4Ghz mobility socket,
    Connect to serial for a 433.000Mhz connection to our mobility code,
    and to accept a connection from a 433.400Mhz relay if we want to double the distance of our rover.
"""

from threading import Thread
from deepstream import get
from time import sleep
import socket
import sys
from relayFunctions import ep
import re
import serial
import os

regex = r"([a-z])(-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,}),(\d{1,}\.?\d{1,}?)#"

ghzMessageAlpha   = [ 'a', '0,0,0,0,0,0,0,0,0,0', str(ep()) ]
hamMessageBravo   = [ 'b', '0,0,0,0,0,0,0,0,0,0', str(ep()) ]
hamMessageCharlie = [ 'c', '0,0,0,0,0,0,0,0,0,0', str(ep()) ]

mode = {}

# this function returns the regular expression class
# which is stored into an array after the function is called
# The other function use the fMessage.group(#) to pull from the regular expressions
# three groups ['a',           '0,0,0,0,0,0,0,0,0,0,'              '######.#####'     ]
#              [ an alpha char, The str to be sent to the arduino, A number relative seconds passed since 12am California time ]
# The reason to use time passed since 6am is to shorten the timestamp to send over the air.
# This saves 160 bytes being sent over the air, shortening epoch time down from a 10 digit length to 5 digits long.
def filterData(s):
    if re.search(regex, s):
      r = re.search(regex, s)
      return r
    else:
      return ""

# Ghz Socket Connection
def connectionToGhzAlpha():
    # Create a TCP/IP socket for the base
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = ('localhost', 5004)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    global ghzMessageAlpha
    while True:
        d, address = sock.recvfrom(512)
        #print(d)

        if d:
            try:
              sent = sock.sendto('r', address)
            except:
              print("couldn't send message back to base")

            try:
              fMessage = filterData(d)
              if fMessage != '':
                ghzMessageAlpha = [ fMessage.group(1), fMessage.group(2), fMessage.group(3) ]
                #print("Ghz:", ghzMessage)
            except:
                pass

# Ham Serial Connection - bravo (433Mhz, channel 0)
def connectionToHamBravo():
    consecutiveMessages = ['-', '-']
    mod2 = 1
    global hamMessageBravo
    while True:
        mod2 = (mod2 + 1) % 2
        try:
          ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
        except:
          #print("cannot connect to serial device")
          pass
        
        try:
          message = ser.read_all()
          print(message)
          try:
            fMessage = filterData(message)
            if fMessage != "":
                hamMessageBravo = fMessage
                print(hamMessageBravo)
                #print("Ham:", hamMessage)
            else:
                consecutiveMessages[mod2] = message
                fMessage = filterData(consecutiveMessages[0] + consecutiveMessages[1])
                print(hamMessageBravo)
                if fMessage != "" and mod2 == 1:
                    hamMessageBravo = fMessage
          except:
            pass
        

        
        except:
            #print("could not read serial device")
            pass
        sleep(0.4)


def sendLatestMessage():
    # Create a TCP/IP socket to the arduino
    sockArd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    arduino_address = ('192.168.1.10', 5000)
    #sockArd.bind(arduino_address)
    sockArd.settimeout(0.25)
    global ghzMessageAlpha, hamMessageBravo, mode
    try:
        sockArd.sendto('0,0,0,0,0,0,0,0,0,0', arduino_address)
    except:
        print("Could not make initial connection to the arduino...")
    while True:
        # Ternary operator to check the time stamp of the message
        message = ghzMessageAlpha if ep() - float(ghzMessageAlpha[2]) < ep() - float(hamMessageBravo[2]) else hamMessageBravo
        # Ternary operator to check if elapsed time is greater than 2 seconds
        print("messageTimeDiff:", ep() - float(message[2]))
        message = message if ep() - float(message[2]) < 2 else ['not receiving data from anything', '0,0,0,0,0,0,0,0,0,0', str(ep() + 10)]
        
        print('Message:', message)
        try:
            d = sockArd.recvfrom(512)[0]
        except:
            d = None
            print("Did not get a message back from the arduino")
        # The message that will get sent to the arduino
        if d == 'r' and ep() - float(message[2]) < 2:
            try:
                if mode != {}:
                    if mode["mode"] == 'manual':
                        sockArd.sendto(message[1], arduino_address)
                    else:
                        print("Mode is not manual")
                else:
                    print("mode is not yet been set to manual")
            except (BlockingIOError, socket.timeout, OSError):
                print("couldn't send message to arduino")
        else:
            sleep(.1)
            sockArd.sendto(message[1], arduino_address)
        

def getDataFromDeepstream():
    global mode
    while True:
        try:
            m = get('mode')
            if type(m) == dict:
                mode = m
                print(mode)
        except:
            pass
        sleep(.8)
        

if os.environ["roverType"] == "rover":
    t1 = Thread(target = connectionToGhzAlpha)
    t2 = Thread(target = connectionToHamBravo)
    t3 = Thread(target = sendLatestMessage)

    t5 = Thread(target = getDataFromDeepstream)

    t1.start()
    t2.start()
    t3.start()

    t5.start()
