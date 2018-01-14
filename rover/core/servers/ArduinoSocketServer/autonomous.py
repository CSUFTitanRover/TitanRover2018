from socket import *
from datetime import datetime
from time import sleep
import json
import requests
import threading, sys #, time ,pygame , RPi.GPIO as GPIO, numpy as np

# Arduino address and connection info
address = ("192.168.1.177", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

GNSS = {'lat':0, 'lon':0}

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
        try:
            payload = {"body":[{"topic": "record", "action":"read", "recordName": "reach/gps"}]}
            request = requests.post('http://127.0.0.1:4080', json=payload)
            if type(request.content) is bytes:
                response = json.loads(request.content.decode('utf-8'))
            elif type(request.content) is str:
                response = json.loads(request.content)

            if response["result"] == "SUCCESS":
                GNSS['lat'], GNSS['lon'] = response["body"][0]["data"]['lat'], response["body"][0]["data"]['lon'] 
            elif response["result"] == "FAILURE":
                print("NO_RECORD")
            
            print(GNSS)
        except:
            pass

Reach = threading.Thread( target = getDeepStreamCurrent, name = 'ReachSystem')
    
#def getCurrentDirection():

#def getDirectionNeeded():

#def getGPS():

def main():
    Reach.start()

if __name__ == "__main__":
    main()

 