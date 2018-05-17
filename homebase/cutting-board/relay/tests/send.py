#!/usr/bin/python
#sends data to a uart rf module
import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
# the library, though you import "serial," is installed using pip install pyserial
# read example
#while True:
#    n = ser.read_all()
#    print(n)
#    time.sleep(.06)

#serial write example:
ser.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
ser.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0

while True:
    ser.write('hello')
    print("sending")
    ser.write('world')
    sleep(0.5)
#while True:
#    ser.write('hello')
#    print("sent\n")
#    #time.sleep(0.2)
