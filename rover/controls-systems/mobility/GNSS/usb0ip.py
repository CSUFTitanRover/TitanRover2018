from subprocess import Popen
from time import sleep


while True:
        Popen(["ifconfig", "usb0", "192.168.2.2"])
        sleep(5)