import serial
from time import sleep
import subprocess


while True:
    try:
        serial.Serial('/dev/tty-emlid', baudrate=115200)
        subprocess.call(["ifconfig", "usb0", "192.168.2.2"])
        subprocess.call(["ifconfig", "-a"])
        while True:
            try:
                subprocess.Popen(["python", "usb0ip.py"])
                subprocess.call(["ssh", "-L", "8000:localhost:80", "root@192.168.2.15"])
                subprocess.call(["python", "reach.py"])
            except:
                print("SSH Connection cannot be established")
                sleep(1)
    except:
        print("Not Connected to the Reach on /dev/ttyACM*")
        sleep(5)
