#!/usr/bin/python
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
#while True:
#    n = ser.read_all()
#    print(n)
#    time.sleep(.06)

#serial write example:
ser.write('AT')
print("sent\n")
time.sleep(1)
