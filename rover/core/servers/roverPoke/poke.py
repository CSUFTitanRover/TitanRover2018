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
    # Get deepstream record named poke
    poke = get('poke')
    if 'poke' in poke:
        # If poke is true, write poke bytes to serial
        if poke['poke'] == True:
            # This sequence matches poke_receive.py, acts as an enclosed buffer to prevent misfires
            print('Writing poke sequence, finger extended')
            ser.write('\n')
            ser.write('p')
            ser.write('o')
            ser.write('k')
            ser.write('e')
            # Post to deepstream that the record is false to stop repeat firing of finger
            post({ 'poke' : False }, 'poke')