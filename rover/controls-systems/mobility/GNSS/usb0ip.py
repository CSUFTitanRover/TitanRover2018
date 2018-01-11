import netifaces as ni
from subprocess import Popen, PIPE
from time import sleep



while True:
    try:
        Popen(["ifconfig", "usb0", "192.168.2.2"])
        sleep(5)
    except:
        print("No Such Device")
