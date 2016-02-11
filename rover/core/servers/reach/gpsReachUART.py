"""
  Richard Stanley
  Rover Socket bind to port 9000. correction data is forwarded over UART

  crontab command to add to rover for startup:
  For nvidia:
  @reboot root cd /home/nvidia/TitanRover2018/rover/core/servers/reach/ && screen -dmS reach && screen -S reach -X stuff "python reach.py \015";
  For pi:
  @reboot root cd /home/pi/TitanRover2018/rover/core/servers/reach/ && screen -dmS reach && screen -S reach -X stuff "python reach.py \015";

"""
import socket
import requests
from threading import Thread
import os
from serial import Serial
from time import sleep, time
from subprocess import Popen, PIPE
import sys
import re

sleep(10)

device = '/dev/serial/by-id/usb-Silicon_Labs_reach_9000-if00-port0'
nvidiaIp = "localhost"
pattern = re.compile('(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
nmeaRegex = r"^(\$[\w,.-\\*-]+)"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1)
server_address = ('0.0.0.0', 9000)
try:
    ser = Serial(device, 57600, timeout=.1)
except:
    print('could not connect to device:', device)
print('starting socket...')
try:
    sock.bind(server_address)
except:
    c = 1
    while True:
        try:
            sock.bind(server_address) 
            break   
        except:
            print('Trying to bind to port 9000, attempts:', c)
            c = c+1
        sleep(1)

print('listening to socket 9000, and sending/reading to/from UART')

nmea = ''
serialData = ''

def socketConnection():
    global nmea, ser
    data = None
    sock.listen(5)
    #connection, client_address = sock.accept()
    try:
        while True:
            try:
              connection, client_address = sock.accept()
              data = connection.recv(4096)
            except:
              pass

            if data:
                print(data)
                try:
                    ser.write(data)
                except:
                    pass
                if nmea != '':
                    connection.sendall(nmea)
                    nmea = ''
                data = None
            else:
                pass
            sleep(0.05)
    except KeyboardInterrupt:
        print('interupted')
        sock.close()





def serialConnection():
    global ser, serialData, nmea
    ser = Serial(device, 57600, timeout=.1)
    try:
        while True:
            try:
                ser = Serial(device, 57600, timeout=.1)
            except:
                pass
            try:
                serialData = ser.readline()
                if serialData != '':
                    #print(serialData)
                    pass
                print(serialData)
            except:
                print('could not find serial device:', device)
                serialData = ''
            
            m = re.match(pattern, serialData)
            if m:
                t = round(time(), 3)
                payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/reach", 
                "data": {"lat": float(m.group(3)), "lon": float(m.group(4)),
                "altitude": float(m.group(5)), "fix": (True if (int(m.group(6)) > 0) else False),
                "nos": int(m.group(7)), "sdn":float(m.group(8)), 
                "sde": float(m.group(9)), "sdu":float(m.group(10)),
                "sdne":float(m.group(11)), "sdeu":float(m.group(12)),
                "sdun":float(m.group(13)), "age":float(m.group(14)), 
                "ratio":float(m.group(15)), "time": t }} ]}
                try:
                    request = requests.post('http://' + nvidiaIp + ':4080', json=payload)
                    print request.text
                except:
                    print("Deepstream doesn't seem to be online")
                
                
                sys.stdout.write(m.group(1) + ' ' + m.group(2) + ' ' + m.group(2) + ' '
                + m.group(3) + ' ' + m.group(4) + m.group(5) + ' ' + m.group(6) + ' ' 
                + m.group(7) + ' ' + m.group(8) + ' ' + m.group(9) + ' ' + m.group(10) + ' ' 
                + m.group(11) + ' '+ m.group(12) + ' '+ m.group(13) + ' ' + m.group(14) + ' '
                + m.group(15) + ' '+ '\n')
            
            try:
                if re.search(nmeaRegex, serialData):
                    r = re.search(nmeaRegex, serialData)
                    nmea = r.groups()[0]
            except:
                pass
            sleep(0.05)
    except KeyboardInterrupt:
        print('interupted')

t1 = Thread(target=socketConnection)
t2 = Thread(target=serialConnection)
t1.daemon=True
t2.daemon=True
t1.start()
t2.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print(' Interrupted! ')
    sock.close()
