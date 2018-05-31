#!/usr/bin/python3
#receives data from a uart rf module and prints what it gets
import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
def pnw(): #testing function reads all from buffer and prints its length and contents
    n = ser.read_all()
    print(len(n))
    print(n)
    sleep(0.5)

def getRF(rf_uart, size_of_payload): #added argument to make it more function-like
    ser.setDTR(True) #if the extra pins on the ttl usb are connected to m0 & m1 on the ebyte module
    ser.setRTS(True) #then these two lines will send low logic to both which puts the module in transmit mode 0
    while True:
        n = rf_uart.read(1) #read bytes one at a time
        if n == b's': #throw away bytes until start byte is encountered
            data = ser.read(size_of_payload) #read fixed number of bytes
            n = ser.read(1) #the following byte should be the stop byte
            if n == b'f':
                print('success')
                print(data)
            else: #if that last byte wasn't the stop byte then something is out of sync
                print("failure")
                return -1
    return data
print("start")
while True:
    #pass serial object to receive from
    #and size of payload IN BYTES
    serial_data = getRF(ser, 2) #returns a tuple of sent variables
    print(serial_data)
