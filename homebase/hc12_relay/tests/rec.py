#!/usr/bin/python
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
# the library, though you import "serial," is installed using pip install pyserial
# read example
ser.setDTR(True)
ser.setRTS(True)
while True:
    n = ser.read_all()
    print(n)
    print("\n")
    #time.sleep(.5)

#serial write example:
#while True:
#    ser.write(0x11111111)
#  print("sent\n")
#   time.sleep(1)
