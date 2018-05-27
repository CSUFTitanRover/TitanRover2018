#!/usr/bin/python3
#sends data to a uart rf module
import serial
from time import sleep
import struct
ardName = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85439313330351D0E102-if00'
ardName2 = 'dev/ttyACM0'
ser = serial.Serial(ardName, 9600, timeout=None)

def putRF(rf_uart, data): #arguments to make function more self-contained and function-like
    rf_uart.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
    rf_uart.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0

    rf_uart.write(b's') #start byte
    rf_uart.write(data) #payload
    rf_uart.write(b'f') #end byte
    rf_uart.flush() #waits until all data is written

#pretend these ints were populated throughout the program
int1, int2, int3, int4, int5, int6, int7, int8, int9, int10 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

#it is probably easiest to pack everything before you pass it to putRF()
data = struct.pack('10b', int1, int2, int3, int4, int5, int6, int7, int8, int9, int10)

#now pass the data to putRF
print("init pause")
sleep(15)

data = 90000
print("write center to ard")
ser.write(struct.pack("i", data))

sleep(15)
data = 45000
print("write left to ard")
ser.write(struct.pack("i", data))

sleep(15)
data = 135000
print("write right to ard")
ser.write(struct.pack("i", data))
while True:
    sleep(15)

