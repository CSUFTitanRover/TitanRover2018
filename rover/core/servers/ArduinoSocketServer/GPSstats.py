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

def getDeepStreamCurrent():
    global GNSS
    while True:

        for i in range(100):
            post({"lat": i ,"lon": i+250}, "GNSS")
       
            GPS = get("GNSS")
            #GNSS['lat'],GNSS['lon'] = GPS["data"]["lat"], GPS["data"]["lon"]
            sleep(.04)
            print(GPS['lat'])
            i += 10

Reach = threading.Thread( target = getDeepStreamCurrent, name = 'ReachSystem')
    
def main():
    Reach.start()

if __name__ == "__main__":
    main()

 