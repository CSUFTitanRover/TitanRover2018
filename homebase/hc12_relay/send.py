#!/usr/bin/python
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 1200, timeout=None)
# the library, though you import "serial," is installed using pip install pyserial
# read example
#while True:
#    n = ser.read_all()
#    print(n)
#    time.sleep(.06)

#serial write example:
while True:
    ser.write('hello')
    print("sent\n")
    time.sleep(1)
