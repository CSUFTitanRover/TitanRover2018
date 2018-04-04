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
hasMovement = False
shouldGoToPoints = False

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

try:
  ser = Serial('/dev/serial/by-id/usb-Silicon_Labs_titan_rover_1002-if00-port0', 9600, timeout=None)
except:
  print("cannot connect to serial device")
  pass

def connectionToHamBravo():
    global hamMessageBravo
    message = ''
    consecutiveMessages = ['\x00', '\x00']
    mod2 = 1
    
    while True:
      try:
        message = ser.read_all()
      except:
        print('not reading serial device')
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
  
def sendLatestMessage():
    global hasMovement, shouldGoToPoints
    # Create a TCP/IP socket to the arduino
    sockArd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    arduino_address = ('192.168.1.10', 5000)
    deadData = "0,0,0,0,0,0,0,0,0,0"
    #sockArd.bind(arduino_address)
    sockArd.settimeout(10)
    global ghzMessageAlpha, hamMessageBravo, autonomousMessage, mode
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
    global mode, gpsManual, shouldGoToPoints
    while True:
        try:
          m = get('mode')
          if type(m) == dict and "mode" in m:
            mode = m
            #print(mode)
        except:
          pass
        sleep(.05)

        try:
          p = get('gpsManual')
          if type(p) == dict:
            if 'points' in p:
              if len(p['points']) > 0:
                if not shouldGoToPoints:
                  gpsManual = p['points']
        except:
          pass
        sleep(.05)
        
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

  


# left or right function will check to make sure the range for the arm movements are ok
def lor(am, p):
  if p < 0 and p < o:
    pass


# for record, 'potentiometers', something like this: { 'pot1': 1000, 'pot2': 684, 'pot3': 983, 'pot4': 763 }
def dontLetTheArmGetFuckedUp(p, armMovements):
  armOffset1 = 500
  armOffset2 = 500
  armOffset3 = 500
  armOffset4 = 500
  if len(armMovements) == 4:
    if type(p) == dict and p != {}:
      if 'pot1' in p and 'pot2' in p and 'pot3' in p and 'pot4' in p:
        if type(p['pot1']) == float and type(p['pot2']) == float and type(p['pot3']) == float and type(p['pot4']) == float:
          v1 = p['pot1'] - armOffset1
          v2 = p['pot2'] - armOffset2
          v3 = p['pot3'] - armOffset3
          v4 = p['pot4'] - armOffset4

  return None

  
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

    t1.start()
    t2.start()
    t3.start()
    t4.start()
else:
    print("You need to set the environment variable roverType=\"rover\"")
