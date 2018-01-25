# -*- encoding: utf-8 -*-

from socket import *
from deepstream import get, post
from datetime import datetime
from time import time, sleep
import threading, sys #, time ,pygame , RPi.GPIO as GPIO, numpy as np
import math
import numpy as np

# Arduino address and connection info
address = ("192.168.1.177", 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)

GNSS = {'lat':0, 'lon':0}
DD_lat = 0
DD_lon = 0
EarthRadius = 6378.1    #In KM
INPUT_MODE = "DD" #[DD] for decimal degrees or [DMS] for degree minutes seconds
generate_destination_times = []

if (INPUT_MODE == "DMS"):           
    post({"lat":"33° 52' 54.7\" N","lon":"117° 53' 04.2\" W"}, "GNSS")         #DMS Format
if (INPUT_MODE == "DD"):
    post({"lat":"33.881860","lon":"-117.884492"}, "GNSS")                      #DD Format

def getDeepStreamCurrent():
    global INPUT_MODE
    global GNSS
    global DD_lat
    global DD_lon
    while True:     
        
        GPS = get("GNSS")                           #Grab from Deepstream

        if (INPUT_MODE == "DMS"):
            DD_lat = DMS_to_DD(GPS['lat'])
            DD_lon = DMS_to_DD(GPS['lon'])             
        elif (INPUT_MODE == "DD"):
            DD_lat = GPS['lat']                  
            DD_lon = GPS['lon']
            DD_lat = float(DD_lat)
            DD_lon = float(DD_lon)
        else:
            print("GPSstats.py failed to run! INPUT_MODE needs to be valid.")
            exit()

        report_current_position()
        sleep(.5)
        generate_destination(180,786.0792)

Reach = threading.Thread( target = getDeepStreamCurrent, name = 'ReachSystem')

def generate_destination(DD_Bearing,CM_Distance): #Bearing [0 = North, 90 = East, 180 = South, 270 = West]
    start = time()
    RAD_Bearing = DEG_to_RAD(DD_Bearing)
    KM_Distance = CM_to_KM(CM_Distance)
    lat1 = math.radians(DD_lat)         
    lon1 = math.radians(DD_lon)

    lat2 = math.asin( math.sin(lat1)*math.cos(KM_Distance/EarthRadius) +
        math.cos(lat1)*math.sin(KM_Distance/EarthRadius)*math.cos(RAD_Bearing))

    lon2 = lon1 + math.atan2(math.sin(RAD_Bearing)*math.sin(KM_Distance/EarthRadius)*math.cos(lat1),
                math.cos(KM_Distance/EarthRadius)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    end = time()
    generate_destination_times.append(round((end-start), 6))
    print("Destination:\t",lat2,',',lon2,"\t Average Calculation Time (seconds)",np.mean(generate_destination_times))    

def CM_to_KM(cm):                       #Centimeters to kilometers
    return(cm/100000)

def DEG_to_RAD(degrees):                #Degrees to radians
    return ((degrees/180)*3.14159265359)

def report_current_position():
    print("Current:\t",DD_lat,',',DD_lon)

def DMS_to_DD(DMS):                     #Degrees/minutes/seconds to Decimal Degrees
    for i in range(0,len(DMS)):         #Remove degree symbol
        if DMS[i] == '°':
            DMS = DMS[:i] + DMS[i+1:]
            break
    for i in range(0,len(DMS)):         #Remove minute symbol
        if DMS[i] == "'":
            DMS = DMS[:i] + DMS[i+1:]
            break
    for i in range(0,len(DMS)):         #Remove second symbol
        if DMS[i] == '"':
            DMS = DMS[:i] + DMS[i+1:]
            break
    DMS = DMS.split()                   #Split DMS string at WHITESPACEs
    degrees = float(DMS[0])
    minutes = float(DMS[1])
    seconds = float(DMS[2])
    cardinal = DMS[3]
    DD = degrees + (minutes/60) + (seconds/3600)
    if(cardinal=='W' or cardinal=='S'):
        DD=(-1)*(DD)
    return DD

def main():
    Reach.start()

if __name__ == "__main__":
    main()

 