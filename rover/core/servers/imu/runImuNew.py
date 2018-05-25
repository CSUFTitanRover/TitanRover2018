# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import sys
import subprocess
import time
from threading import Thread
import socket
import requests
#from deepstream import get, post
from Adafruit_BNO055 import BNO055

global imuData
imuData = {}

HOST = ''
PORT = 8090
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        print("Trying to bind")
        SERVER.bind(ADDR)
        Print("binding complete")
        break
    except:
        subprocess.call(' sudo lsof -t -i tcp:8090 | xargs kill -9', shell = True)

def postToDeepstream():
    global imuData
    while True:
        payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/imu", 
                    "data": imuData} ] }

        try:
            print("Dumping to deepstream...")
            #request = requests.post('http://192.168.1.8:3080', json=payload)
            #print request.text
            time.sleep(5)
        except:
            print("Deepstream doesn't seem to be online")

#subprocess.call(["python3.5", "calImu.py"])
#time.sleep(3)

'''
try:
    obj = {}
    post(obj, 'imu')
except:
    print("Not connected to deepstream")
'''
magneticDeclination = 11.88

# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
#bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
# BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
# and RST connected to pin P9_12:
bno = BNO055.BNO055(busnum=0)
confMode = True

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

time.sleep(1)
# Initialize the BNO055 and stop if something went wrong.
while not bno.begin():
    print('Waiting for sensor...')
    time.sleep(1)

def magToTrue(h):
    return (h + magneticDeclination) % 360

fileIn = open('calibrationData.txt','r')
data = fileIn.read().splitlines()
for i in range(len(data)):
    data[i] = int(data[i])
bno.set_calibration(data)
fileIn.close()

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')

while True:
    print("connecting")
    time.sleep(3)
    client, client_address = SERVER.accept()
    print("%s:%s has connected." % client_address)


try:
    Thread(target=postToDeepstream).start()
    while True:
        '''
        if confMode == False and (sys != 3 or mag != 3):
            print("Reloading calibration file...")
            bno.set_calibration(data)
        '''
        
        # Read the Euler angles for heading, roll, pitch (all in degrees)
        heading, roll, pitch = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated
        sys, gyro, accel, mag = bno.get_calibration_status()
        heading = magToTrue(heading)
       
        if sys == 3 and gyro == 3 and accel == 3 and mag == 3 and confMode:
            bno.set_mode(0X0C)
            confMode = False

        #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
        #    heading, roll, pitch, sys, gyro, accel, mag))

        imuData = { "heading":heading, "roll":roll, "pitch":pitch, "sys":sys, "gyro":gyro, "accel":accel, "mag":mag }
        temp = imuData['heading']
        client.send(temp)
        '''
        try:
            response = post({ "heading":heading, "roll":roll, "pitch":pitch, "sys":sys, "gyro":gyro, "accel":accel, "mag":mag }, 'imu')
        except:
            print("Cannot Post to Deepstream")            
        response = None
        '''
        # Other values you can optionally read:
        # Orientation as a quaternion:
        #x,y,z,w = bno.read_quaterion()
        # Sensor temperature in degrees Celsius:
        #temp_c = bno.read_temp()
        # Magnetometer data (in micro-Teslas):
        #x,y,z = bno.read_magnetometer()
        # Gyroscope data (in degrees per second):
        #x,y,z = bno.read_gyroscope()
        # Accelerometer data (in meters per second squared):
        #x,y,z = bno.read_accelerometer()
        # Linear acceleration data (i.e. acceleration from movement, not gravity--
        # returned in meters per second squared):
        #x,y,z = bno.read_linear_acceleration()
        # Gravity acceleration data (i.e. acceleration just from gravity--returned
        # in meters per second squared):
        #x,y,z = bno.read_gravity()
        # Sleep for a second until the next reading.
        time.sleep(0.02)
except:
    print("Error")
    client.close()


