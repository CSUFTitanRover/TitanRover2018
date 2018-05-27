'''
Titan Rover 2018
Maxfield Wilhoite

Poke Script
Sends sequence to receiver to extend the finger
'''

from deepstream import get, post
from time import sleep
from serial import Serial
#from threading import Thread

# Connect to COM port, need to change the first parameter to match USB com port the poke board is attached to
try:
    ser = Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0', 9600)
except:
    print("cannot connect to serial device.")
    
# Loop while script is running, waiting for deepstream update sent by basestation
while True:
    try:
        ser = Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0', 9600)
    except:
        print("cannot connect to serial device.")
    poke = {'poke' : True}
    if 'poke' in poke:
        # If poke is true, write poke bytes to serial
        if poke['poke'] == True:
            #print('POKE!!')
            for x in range(5):
                ser.write('1')
                print("1")
            for y in range(5):
                ser.write('0')
                print("0")
            sleep(0.05)
            #post({ 'poke': False }, 'poke', 'localhost')
            sleep(0.9)
    sleep(0.05)
