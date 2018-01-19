import serial
from deepstream import get, post
from time import sleep

device = "/dev/oled1"
baud = 9600


numOfRecords = 7

heading = " NOREC"
pitch =   " NOREC"
roll =    " NOREC"
mcal =    " NOREC"
dl =      " NOREC"
ul =      " NOREC"
ip =      "           NOREC"


toSend =  "Loadng"*6 + " "*6 + "Loadng"

while True:
    try:
        ser = serial.Serial(device, baud, timeout=.5)
    except:
        print("cannot connec to serial device: "+ device)
    try:
        d = get("imu")
        heading = "{:3.1f}".format(float(d["heading"])).rjust(6)
        pitch =   "{:3.1f}".format(float(d["pitch"])).rjust(6)
        roll =    "{:3.1f}".format(float(d["roll"])).rjust(6)
        mcal =    ("yes" if int(d["mag"]) is 3 else "no").rjust(6)
    except:
        heading = " NOREC"
        pitch =   " NOREC"
        roll =    " NOREC"
        mcal =    " NOREC"
    try:
        iftop = get("speed")
        if iftop is not {} or iftop is not "NO_RECORD":
            ip = str(iftop["ip"]).rjust(12)[-12:]
           

            if (iftop["download"] > 1000000):
                dl = "{:3.0f}".format(iftop["download"] /1000000).rjust(4) + "Mb"
                
            elif(iftop["download"] > 1000):
                dl = "{:3.0f}".format(iftop["download"] /1000).rjust(4) + "Kb"
                
            else:
                dl = "{:3.0f}".format(iftop["download"]).rjust(5) + "b"
                
            if (iftop["upload"] > 1000000):
                ul = "{:3.0f}".format(iftop["upload"] /1000000).rjust(4) + "Mb"
                
            elif(iftop["upload"] > 1000):
                ul = "{:3.0f}".format(iftop["upload"] /1000).rjust(4) + "Kb"
                
            else:
                ul = "{:3.0f}".format(iftop["upload"]).rjust(5) + "b"
        else:
            dl =      " NOREC"
            ul =      " NOREC"
            ip =      " "*10 + " NOREC"
    except:
        dl =      " NOREC"
        ul =      " NOREC"
        ip =      " "*10 + " NOREC"

    toSend0 = heading + pitch + roll + mcal + dl + ul + ip
    print(toSend0)
    try:
        ser.write(toSend0)
    except:
        print("serial device: " + device + " Not communicating")
    sleep(.09)
