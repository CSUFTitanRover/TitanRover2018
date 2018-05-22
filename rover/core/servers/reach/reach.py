#!/usr/bin/python

import serial
from time import sleep
import re
import sys
import socket
import subprocess
import requests
global ser, nvidiaIp
nvidiaIp = "192.168.1.253"


#sleep(10)
#subprocess.call('echo "1" > /proc/sys/net/ipv4/ip_forward', shell = True)
#subprocess.call('iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -j MASQUERADE', shell = True)

def reach():
    #print("into reach")
    #subprocess.call('echo "1" > /proc/sys/net/ipv4/ip_forward', shell = True)
    #subprocess.call('iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -j MASQUERADE', shell = True)
    try:
        while True:
            try:
                #print("trying to connect")
                proc = subprocess.Popen(['ssh', 'root@192.168.2.15'], stdout = subprocess.PIPE,)
                out = proc.communicate()[0]
                #print(out)
                if "File exists" in out:
                    break
            except:
                #print("pass")
                pass
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('', 7074))
                s.listen(2)
                break
            except:
                subprocess.call(' sudo lsof -t -i tcp:7074 | xargs kill -9', shell = True)
                print("Waiting For Connection")
                sleep(2)


        while True:
            try:
                conn, address = s.accept()
                print("Connection from", address)
                break
            except:
                print("ERROR CONNECTING")
                sleep(3)
            
        pattern = re.compile('(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
        print("Waiting for GPS Lock...")

        while True:
            #data = ser.readline()
            data = conn.recv(2048)
            print(data)
            m = re.match(pattern, data)
            if m:
                payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/gps", 
                "data": {"lat": float(m.group(3)), "lon": float(m.group(4)),
                "altitude": float(m.group(5)), "fix": (True if (int(m.group(6)) > 0) else False),
                "nos": int(m.group(7)), "sdn":float(m.group(8)), 
                "sde": float(m.group(9)), "sdu":float(m.group(10)),
                "sdne":float(m.group(11)), "sdeu":float(m.group(12)),
                "sdun":float(m.group(13)), "age":float(m.group(14)), 
                "ratio":float(m.group(15)) }} ]}
                try:
                    print("Dumping to deepstream...")
                    request = requests.post('http://' + nvidiaIp + ':3080', json=payload)
                    print request.text
                except:
                    print("Deepstream doesn't seem to be online")
                    
                sys.stdout.write(m.group(1) + ' ' + m.group(2) + ' ' + m.group(2) + ' '
                + m.group(3) + ' ' + m.group(4) + m.group(5) + ' ' + m.group(6) + ' ' 
                + m.group(7) + ' ' + m.group(8) + ' ' + m.group(9) + ' ' + m.group(10) + ' ' 
                + m.group(11) + ' '+ m.group(12) + ' '+ m.group(13) + ' ' + m.group(14) + ' '
                + m.group(15) + ' '+ '\n')
                    
            else:
                print("No valid regex data")
                s.close()
                break

            print(data)
    except KeyboardInterrupt:
        #s.close()
        pass

while True:
    reach()

