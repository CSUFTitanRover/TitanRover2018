from socket import *
from deepstream import get, post
from datetime import datetime
from time import sleep
import threading, sys #, time ,pygame , RPi.GPIO as GPIO, numpy as np

# Arduino address and connection info
address = ("192.168.1.177", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

GNSS = {'Lat':0, 'Lon':0}

# LED status signals
'''GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
redLed = 18
greenLed = 23
blueLed = 24
GPIO.setup(redLed, GPIO.OUT)  # Red LED
GPIO.setup(greenLed, GPIO.OUT)  # Green LED
GPIO.setup(blueLed, GPIO.OUT)  # Blue LED'''

#def functName(arg1, arg2)
#t = threading.Thread(  target  = functName, 
#                       name    = 'threadName', 
#                       args    = (arg1Val, arg2Val))
#t.start()
#thread_list[] ----maybe useful
#
#for i in range(5)
#   t.threading.Thread( target  = functName, 
#                       name    = 'threadName{}'.format(i), 
#                       args    = (arg1Val, arg2Val))
#   threads_list.append(t)
#   t.start()

def getDeepStreamCurrent():
    global GNSS
    while True:
        GPS = get("GNSS")
        GNSS['lat'],GNSS['lon'] = GPS["data"]["lat"], GPS["data"]["lon"]
        sleep(.04)
        print(GNSS)

Reach = threading.Thread( target = getDeepStreamCurrent, name = 'ReachSystem')
    
#def getCurrentDirection():

#def getDirectionNeeded():

#def getGPS():

def main():
    Reach.start()

if __name__ == "__main__":
    main()

 