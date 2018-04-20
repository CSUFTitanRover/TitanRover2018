"""
    Richard Stanley
    TitanRover 2018
    The purpose of this code is to hold a socket connection out 3.4Ghz mobility socket,
    Connect to serial for a 433.000Mhz connection to our mobility code,
    and to accept a connection from a 433.400Mhz relay if we want to double the distance of our rover.
"""
from sys import getsizeof
from autonomousCore import Driver
from struct import *
from threading import Thread
from deepstream import get, post
from subprocess import Popen, PIPE
from time import sleep, time
import math
from sqlFunctions import storeMessage
import socket
import sys
import re
from serial import Serial
import os


myDriver = Driver()
regex = r"([a-z])(-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,},-?\d{1,}),(-?\d{1,}\.?\d{1,}?)#"
byteRegex = re.compile(b'a[\0-\xFF]{20,60}#$')

initialTimeStamp = time()
ghzMessageAlpha   = [ 'a', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
hamMessageBravo   = [ 'b', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
autonomousMessage = [ 'c', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
message           = [ 'a', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]

hasMovement = False
shouldGoToPoints = False
currentLocation = None

# SET THE MODE TO MANUAL TEMPORARILY
# post({"mode": "manual"}, "mode")

mode = {}
gpsManual = []

# this function returns the regular expression class
# which is stored into an array after the function is called
# The other function use the fMessage.group(#) to pull from the regular expressions
# three groups ['a',           '0,0,0,0,0,0,0,0,0,0,'              '######.#####'     ]
#              [ an alpha char, The str to be sent to the arduino, epoch timestamp in seconds, rounded 3 decimal places ]
# This saves 160 bytes being sent over the air, shortening epoch time down from a 10 digit length to 5 digits long.
def filterData(s):
    if re.search(regex, s):
      r = re.search(regex, s)
      return r
    else:
      return ""


def depackageByteData(d):
  """
    This function takes a bytearray, and depackages the
    byte array as long as it matches the exact format comming
    from the mobility code.
    an example:
      packed bytearray with the format 's 10h d s'
      please see python documentation on the struct library
        'pack' and 'unpack' modules
  """
  print(d)
  h = bytearray()
  #if re.search(byteRegex, d):
  begin = False
  for k in d:
    if k == 'a' or k == 'b' or k == 'c' and begin == False:
      h.append(k)
      begin = True
    elif k == '#' and begin == True:
      h.append(k)
      break
    elif begin == True:
      h.append(k)
  a = None
  try:
    a = unpack('s 10h d s', h)
  except:
    #print("could not unpack the data from message")
    pass
  return a


"""

  Ghz Socket Connection

"""
def connectionToGhzAlpha():
    global ghzMessageAlpha, autonomousMessage

    while True:
        #print("GHZ LOOP")
        d, address = sock.recvfrom(512)
        #d = str(d.decode('utf-8'))
        #print("Directly from mobility:", d)
        if d:
          f = depackageByteData(d)
          #print(f)
          if f != None:
            f = [f[0], ','.join(list(map(str, f[1:11]))), f[11]]
            if f[0] == 'a':
              ghzMessageAlpha = f
            elif f[0] == 'c':
              autonomousMessage = f
            #print(f)


"""

  Ham Serial Connection - bravo (433Mhz, channel 0)

"""

def connectionToHamBravo():
    global hamMessageBravo
    message = ''
    consecutiveMessages = ['\x00', '\x00']
    mod2 = 1
    
    while True:
      try:
        message = ser.read_all()
      except:
        try:
          ser = Serial('/dev/serial/by-id/usb-Silicon_Labs_titan_rover_433-if00-port0', 9600, timeout=None)
        except:
          pass
      if message != '':
        print(message)
      f = depackageByteData(message)
      consecutiveMessages[mod2] = message
      if f == None:
        if mod2 == 0:
          f = depackageByteData( consecutiveMessages[1] + message)
          if f != None:
            hamMessageBravo = [f[0], ','.join(list(map(str, f[1:11]))), f[11]]
        elif mod2 == 1:
          f = depackageByteData( consecutiveMessages[0] + message )
          if f != None:
            hamMessageBravo = [f[0], ','.join(list(map(str, f[1:11]))), f[11]]
      else:
        hamMessageBravo = [f[0], ','.join(list(map(str, f[1:11]))), f[11]]
      #print(hamMessageBravo)
      mod2 = (mod2 + 1) % 2
      sleep(.06)

moveRegex = r"(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),(-?\d{1,}),\d{1,}"
def hasSomeMovement(s):
  """
    Description: This function will return True if there is any movement from our mobility code string.
  """
  if re.search(moveRegex, s):
    m = re.search(moveRegex, s).groups()
    m = map(int, m)
    m = reduce(lambda x,y:x+y, m)
    if m != 0:
      return True
  return False

def splitOutData(d):
  if re.search(moveRegex, d):
    m = re.search(moveRegex, s).groups()
    m = map(int, m)
    return m
  return None
  
def sendLatestMessage():
    global hasMovement, shouldGoToPoints
    # Create a TCP/IP socket to the arduino
    sockArd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    arduino_address = ('192.168.1.10', 5000)
    deadData = "0,0,0,0,0,0,0,0,0,0"
    #sockArd.bind(arduino_address)
    sockArd.settimeout(10)
    global ghzMessageAlpha, hamMessageBravo, autonomousMessage, mode, message
    #while True:
    try:
      sockArd.sendto(deadData, arduino_address)
    except:
      print("Could not make initial connection to the arduino...")
    
    while True:
        # Ternary operator to check the time stamp of the message.
        # The greater the number (timestamp), the more recent the timestamp.
        message = ghzMessageAlpha if float(ghzMessageAlpha[2]) >= float(hamMessageBravo[2]) else hamMessageBravo

        if float(autonomousMessage[2]) > float(message[2]) or (float(ghzMessageAlpha[2]) > 10 and float(hamMessageBravo[2]) > 10):
          if 'mode' in mode:
            if mode['mode'] == 'manual':
              shouldGoToPoints = True
              sleep(0.05)
              hasMovement = hasSomeMovement(message[1])
              shouldGoToPoints = False if hasMovement else True
        
        if 'mode' in mode: # autonomous mode in deepstream will always override manual mobility code.
          if mode['mode'] == 'autonomous':
            message = autonomousMessage
        #print('ready for arduino:', message)
        # Ternary operator to check if elapsed time is greater than 1.5 seconds
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
        #print('TIME DIFF:', time() - float(message[2]))
        # The message that will get sent to the arduino
        if time() - float(message[2]) < 1.5: #ep() - float(message[2]) - secondsOffset < 10:
          #try:
            if "mode" in mode:
              if mode["mode"] == 'manual':
                #print(message)
                sockArd.sendto(message[1], arduino_address)
                if(d != 'r'):
                  print("Unsuccessful message sent to arduino")
                else:
                  pass
              elif mode['mode'] == 'autonomous': # handle autonomous code.
                sockArd.sendto(message[1], arduino_address)  
            else:
              print("mode is not yet been set to manual")
          #except:
          #  print("couldn't send message to arduino")
        else:
          sleep(.05)
          sockArd.sendto(deadData, arduino_address)
          ghzMessageAlpha   = [ 'a', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
          hamMessageBravo   = [ 'b', '0,0,0,0,0,0,0,0,0,0', initialTimeStamp ]
          print("timeStamp not less than 3")



def getDataFromDeepstream():
    global mode, gpsManual, shouldGoToPoints, currentLocation
    while True:
        try:
          m = get('mode', 'localhost')
          if type(m) == dict and "mode" in m:
            mode = m
            #print(mode)
        except:
          pass
        sleep(0.05)

        try:
          p = get('gpsManual', 'localhost')
          if type(p) == dict:
            if 'points' in p:
              if len(p['points']) > 0:
                if not shouldGoToPoints:
                  gpsManual = p['points']
        except:
          pass

        sleep(0.05)
        try:
          l = get('reach', 'localhost')
          if type(l) == dict:
            if 'lat' in l and 'lon' in l:
              currentLocation = l
        except:
          pass
        sleep(0.05)

def calculateDistance(p1, p2):
  a1, b1 = p1
  a2, b2 = p2
  radius = 6371 # km

  da = math.radians(a2-a1)
  db = math.radians(b2-b1)
  a = math.sin(da/2) * math.sin(da/2) + math.cos(math.radians(a1)) \
    * math.cos(math.radians(a2)) * math.sin(db/2) * math.sin(db/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = radius * c
  return d * 1000


"""

  This function stores telemetry data to be able to be read ater a long
  day of testing.

"""
def storeData():
  global currentLocation, message
  baseLocation = (0,0)
  while True:
    print('running StoreData:', currentLocation, message)
    if currentLocation is not None:
      if 'lat' in currentLocation and 'lon' in currentLocation:
        t = message[2]
        ghzOrHam = None
        roverLocation = (currentLocation['lat'], currentLocation['lon'])
        distance = calculateDistance(baseLocation, roverLocation)
        print(distance)
        if message[0] == 'a':
          ghzOrHam = 0
        if message[0] == 'b':
          ghzOrHam = 1 
        if ghzOrHam is not None:
          storeMessage(message[2], distance, ghzOrHam)
    sleep(1)
        
def goToWhenConnectionLost():
  global hasSomeMovement, shouldGoToPoints, gpsManual
  while True:
    while len(gpsManual) > 0:
      if shouldGoToPoints and not hasMovement:
        Driver.goTo(gpsManual[-1])
        gpsManual.pop()
      try:
        post({ 'points': gpsManual }, 'gpsManual', 'localhost')
      except:
        pass
  sleep(0.04)
 
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
    t4 = Thread(target = getDataFromDeepstream)
    t5 = Thread(target = storeData)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
  else:
    print('Your roverType is set to base, so socketRelay will not start until roverType is set to: rover')
else:
    print("You need to set the environment variable roverType=\"rover\"")
