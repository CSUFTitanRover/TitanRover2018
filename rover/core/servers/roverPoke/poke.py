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
    poke = {'poke' : True}
    if 'poke' in poke:
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
