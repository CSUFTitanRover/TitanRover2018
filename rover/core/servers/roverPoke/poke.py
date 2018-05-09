from deepstream import get, post
from time import sleep
from serial import Serial
from threading import Thread

sleep(8.5)

while True:
    try:
        ser = Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0', 9600)
    except:
        print("cannot connect to serial device.")
    poke = {'poke' : True}#get('poke', 'localhost')
    if 'poke' in poke:
        if poke['poke'] == True:
            print('POKE!!')
            ser.write('1')
            sleep(2)
            #post({ 'poke': False }, 'poke', 'localhost')
            sleep(0.05)
    sleep(0.05)