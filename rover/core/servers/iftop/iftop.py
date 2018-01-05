#!/usr/bin/python
from time import sleep
from subprocess import call, Popen
from deepstream import post
import subprocess, re

recordName = "speed"
interface = "wlp3s0"

obj = {}
post(obj, recordName)

while True:
    p = Popen([ "iftop", "-o", "10s", "-t", "-s", "10", "-L", "2", "-i", interface ], stdout=subprocess.PIPE)
    out, err = p.communicate()
    try:
        uploadArr = re.findall(r"Total send rate:\s+(\d{1,}\.{0,1}\d{0,})(\w+)", out)
        downloadArr = re.findall(r"Total receive rate:\s+(\d{1,}\.{0,1}\d{0,})(\w+)", out)
        upload = 0
        download = 0
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
            print "Upload: {} {} Download: {} {}".format(upload, uploadArr[0][1], download , downloadArr[0][1])
            post({"upload": upload, "download": download}, recordName)
    except:
        try:
            post({}, "speed")
        except:
            print("cannot connect to deepstream.")
