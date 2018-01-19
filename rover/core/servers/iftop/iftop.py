#!/usr/bin/python
from time import sleep, time
from threading import Thread
from subprocess import call, Popen
from deepstream import post
import subprocess, re

print("Loading: iftop")
recordName = "speed"
interface = "wlp3s0"

# Number in seconds to switch to autonomous/manual Mode
elapsedTimout = 16

obj = {}
success = ""

while success == "":
   try:
       success = post(obj, recordName)
       success = post({"mode": "manual"}, "mode")
   except:
       print("Not connected to deepstream")
   sleep(1)

ipAddress = " NOREC"
upload = 0
download = 0
elapsedTime = 0


def getUpDownData():
    global obj, ipAddress, upload, download, elapsedTime
    while True:
        try:
            # command: sudo iftop -o 10s -t -s 10 -L 1 -i wlp3s0
            elapsedTime = 0
            p = Popen([ "/usr/sbin/iftop", "-o", "10s", "-t", "-s", "10", "-L", "1", "-i", interface ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            out = p[0]
            err = p[1]

            uploadArr = re.findall(r"Total send rate:\s+(\d{1,}\.{0,1}\d{0,})(\w+)", out)
            downloadArr = re.findall(r"Total receive rate:\s+(\d{1,}\.{0,1}\d{0,})(\w+)", out)
            ipAddressArr = re.findall(r"IP address is:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", err)
            if ipAddressArr is not []:
                ipAddress = ipAddressArr[0]
            
            if uploadArr is not [] and downloadArr is not []:
                upload = float(uploadArr[0][0])
                download = float(downloadArr[0][0])
                if uploadArr[0][1] == "Kb":
                    upload = upload * 1000
                if downloadArr[0][1] == "Kb":
                    download = download * 1000
                if uploadArr[0][1] == "Mb":
                    upload = upload * 1000000
                if downloadArr[0][1] == "Mb":
                    download = download * 1000000
                obj = {"upload": upload, "download": download, "ip": ipAddress, "elapsed": elapsedTime}
                #print "upload: {} {} download: {} {} ip: {}".format(upload, uploadArr[0][1], download , downloadArr[0][1], ipAddress)
                dsSuccess = post(obj, recordName)
                print(obj)
            uploadArr = []
            downloadArr = []
        except:
            try:
               post({}, "speed")
               print("No data from interface: " + interface)
               sleep(1)
            except:
               print("cannot connect to deepstream.")


def checkElapsedTime():
    global elapsedTime
    while True:
        elapsedTime = elapsedTime + 1
        if(elapsedTime > 16):
            try:
                post({ "mode": "autonomanual" }, "mode")
                upload = 0
                download = 0
                post({"upload": upload, "download": download, "ip": ipAddress, "elapsed": elapsedTime}, recordName)
            except:
                print("cannot post to deepstream")
        sleep(1)

t1 = Thread(target=getUpDownData)
t2 = Thread(target=checkElapsedTime)

t1.start()
t2.start()
