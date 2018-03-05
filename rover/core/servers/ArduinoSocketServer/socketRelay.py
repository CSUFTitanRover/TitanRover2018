"""
    Richard Stanley
    TitanRover 2018
    The purpose of this code is to hold a socket connection out 3.4Ghz mobility socket,
    Connect to serial for a 433.000Mhz connection to our mobility code,
    and to accept a connection from a 433.400Mhz relay if we want to double the distance of our rover.
"""
import select
from threading import Thread
from deepstream import get, post
from subprocess import Popen, PIPE
from time import sleep
import socket
import sys
from relayFunctions import ep
import re
from serial import Serial
import os

regex = r"([a-z])(-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,}),(-?\d{1,}\.?\d{1,}?)#"

initialTimeStamp = str(ep())
ghzMessageAlpha   = [ 'a', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
hamMessageBravo   = [ 'b', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
hamMessageCharlie = [ 'c', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
secondsOffset = 0

# SET THE MODE TO MANUAL TEMPORARILY
# post({"mode": "manual"}, "mode")

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






"""

  Ghz Socket Connection

"""
def connectionToGhzAlpha():
    global ghzMessageAlpha, secondsOffset

    while True:
        #print("GHZ LOOP")
        d, address = sock.recvfrom(512)
        d = str(d.decode('utf-8'))
        #print("Directly from mobility:", d)
        if d:
            try:
              fMessage = filterData(d)
              #print("DataFromMobility", fMessage.group(2))
              if fMessage != '':
                ghzMessageAlpha = [ fMessage.group(1), fMessage.group(2), fMessage.group(3) ]
                secondsOffset = ep() - float(ghzMessageAlpha[2])
            except:
                print("could not parse the regex")
                pass

            try:
              sent = sock.sendto('r', address)
            except:
              print("couldn't send message back to base")
        else:
          print("Ghz data failed")



"""

  Ham Serial Connection - bravo (433Mhz, channel 0)

"""

try:
  ser = Serial('/dev/serial/by-id/usb-Silicon_Labs_titan_rover_1002-if00-port0', 9600, timeout=None)
except:
  print("cannot connect to serial device")
  pass

def connectionToHamBravo():
    global hamMessageBravo
    consecutiveMessages = ['-', '-']
    mod2 = 1

    while True:
        mod2 = (mod2 + 1) % 2
        try:
          message = ser.read_all()
          message = message.decode('utf-8')
          print("New Ham Message: " + message)
          try:
            fMessage = filterData(message)
            if fMessage != "":
                hamMessageBravo = [ fMessage.group(1), fMessage.group(2), fMessage.group(3) ]
                #print("successful Ham parse:" + hamMessageBravo[1])
                #print("Ham:", hamMessage)
            elif mod2 == 0:
                consecutiveMessages[1] = message
                fMessage = filterData(consecutiveMessages[0] + consecutiveMessages[1])
                print("consecutive string: " + hamMessageBravo)
                if fMessage != "":
                    hamMessageBravo = [ fMessage.group(1), fMessage.group(2), fMessage.group(3) ]
            elif mod2 == 1:
                consecutiveMessages[0] = message
                fMessage = filterData(consecutiveMessages[1] + consecutiveMessages[0])
                print("consecutive string: " + hamMessageBravo)
                if fMessage != "":
                    hamMessageBravo = [ fMessage.group(1), fMessage.group(2), fMessage.group(3) ] 
                    
          except:
            #print("something went wrong with parsing")
            pass
        
        except:
            #print("could not read serial device")
            pass
        sleep(0.08)


def sendLatestMessage():
    zed = [ 'z', '0,0,0,0,0,0,0,0,0,0', str(ep()) ]
    # Create a TCP/IP socket to the arduino
    sockArd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sockArd.setblocking(0)
    #ready = select.select([sockArd], [], [], 1) 
    # Bind the socket to the port
    arduino_address = ('192.168.1.10', 5000)
    data = "0,0,0,0,0,0,0,0,0,0"
    #sockArd.bind(arduino_address)
    sockArd.settimeout(10)
    global ghzMessageAlpha, hamMessageBravo, mode, secondsOffset
    #while True:
    try:
      sockArd.sendto(data, arduino_address)
      #print(data)
    except:
      print("Could not make initial connection to the arduino...")
    
    while True:
        # Ternary operator to check the time stamp of the message.
        # The greater the number (timestamp), the more recent the timestamp.
        message = ghzMessageAlpha if float(ghzMessageAlpha[2]) > float(hamMessageBravo[2]) else hamMessageBravo
        # Ternary operator to check if elapsed time is greater than 2 seconds
        #print("DiffBetweenGhzAndHam:", ep () - float(message[2]) - secondsOffset)
        #message = message if ep() - float(message[2]) - secondsOffset < 3 else zed
        #print(ghzMessageAlpha[2])
        d = None
        #print("waiting for 'r'")
        try:
          d = sockArd.recvfrom(512)[0]
          if d == 'r':
            #print("ARDUINO IS RESPONDING")
            pass
          else:
            #print("ARDUINO IS NOT RESPONDING")
            pass
        except:
            d = None
            #print("Did not get a message back from the arduino")
        #print("Ghz:", ghzMessageAlpha[0] + ghzMessageAlpha[1]+ str(ep() - float(ghzMessageAlpha[2])))
        #print(message)
        # The message that will get sent to the arduino
        if True: #ep() - float(message[2]) - secondsOffset < 10:
          #try:
            if "mode" in mode:
              if ep() - float(message[2]) - secondsOffset < 4:
                if mode["mode"] == 'manual':
                  #print(message)
                  sockArd.sendto(message[1], arduino_address)
                  if(d != 'r'):
                    print("Unsuccessful message sent to arduino")
                  else:
                    #print("GhzTimeDiff: " + str(ep() - float(ghzMessageAlpha[2]) - secondsOffset))
                    #print("HamTimeDiff: " + str(ep() - float(hamMessageBravo[2]) - secondsOffset))
                    #print("Attempted message to arduino: " + message[1])
                    pass
                else:
                  pass
              else:
                  sockArd.sendto('0,0,0,0,0,0,0,0,0,0', arduino_address)
            else:
              print("mode is not yet been set to manual")
          #except:
          #  print("couldn't send message to arduino")
        else:
          sleep(.1)
          sockArd.sendto(data, arduino_address)
          print("timeStamp not less than 3")
          pass
          #sockArd.sendto(message[1], arduino_address) 

def getDataFromDeepstream():
    global mode
    while True:
        try:
            m = get('mode')
            if type(m) == dict and "mode" in m:
                mode = m
                #print(mode)
        except:
            pass
        sleep(.8)
        
if os.getenv("roverType") is not None:
  if os.environ["roverType"] == "rover":
    # Create a TCP/IP socket for the base
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = ('0.0.0.0', 5001)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    # If binding to the socket fails, then we need to reset socket 5001 by killing the processId binded to 5001:
    try:
      sock.bind(server_address)
    except:
      o = Popen(["lsof", "-t", "-i", "udp:5001"], stdout=PIPE, stderr=PIPE).communicate()[0] 
      print('PROCESSNUM: '+ o)
      os.kill(int(o), 9)
      sleep(3)
      sock.bind(server_address) 
      print("SOCKET 5001 WAS RESET. KILLED PID "+o)
      pass

    t1 = Thread(target = connectionToGhzAlpha)
    t2 = Thread(target = connectionToHamBravo)
    t3 = Thread(target = sendLatestMessage)

    t5 = Thread(target = getDataFromDeepstream)

    t1.start()
    t2.start()
    t3.start()

    t5.start()
else:
    print("You need to set the environment variable roverType=\"rover\"")

