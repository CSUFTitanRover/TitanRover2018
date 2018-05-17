#!/usr/bin/python
#receives data from a uart rf module and prints what it gets
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
# the library, though you import "serial," is installed using pip install pyserial
# read example

ser.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
ser.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0

while True:
    n = ser.read_all()
    print(n)
    time.sleep(.5)

#serial write example:
#while True:
#    ser.write(0x11111111)
#  print("sent\n")
#   time.sleep(1)
