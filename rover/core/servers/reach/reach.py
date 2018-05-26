import serial
from time import sleep
import re
import sys
import socket
import subprocess
import requests
from threading import Thread 
global ser, nvidiaIp, gpsPoint
#nvidiaIp = "192.168.1.8"
gpsPoint = ()


def acceptConnections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        Thread(target=broadcastGps, args=(client, )).start()

def broadcastGps(client):
        global gpsPoint
        while True:
            try:
                temp = ",".join(str(x) for x in gpsPoint)
                #print("points = ", temp, "type ", type(temp))
                client.send(temp)
                print("Send to Client Successful")
                sleep(0.5)
            except:
                print("Error sending to client")
                sleep(5)


def reach():
    global gpsPoint
    subprocess.call('echo "1" > /proc/sys/net/ipv4/ip_forward', shell = True)
    #subprocess.call('iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -j MASQUERADE', shell = True)
    try:
        '''
        while True:
            try:
                proc = subprocess.Popen(['ssh', 'root@192.168.2.15'], stdout = subprocess.PIPE,)
                out = proc.communicate()[0]
                if out:
                    break
            except:
                pass
        '''
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
                "data": {"lat": float(m.group(3)), "lon": float(m.group(4))}} ] }

                gpsPoint = (float(m.group(3)), float(m.group(4)))

                '''                
                payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/gps", 
                "data": {"lat": float(m.group(3)), "lon": float(m.group(4)),
                "altitude": float(m.group(5)), "fix": (True if (int(m.group(6)) > 0) else False),
                "nos": int(m.group(7)), "sdn":float(m.group(8)), 
                "sde": float(m.group(9)), "sdu":float(m.group(10)),
                "sdne":float(m.group(11)), "sdeu":float(m.group(12)),
                "sdun":float(m.group(13)), "age":float(m.group(14)), 
                "ratio":float(m.group(15)) }} ]}
                '''
                print("Dumping to deepstream...")
                try:
                    request = requests.post('http://192.168.1.2:4080', json=payload)
                    print(request.text)
                except:
                    print("Rover Deepstream doesn't seem to be online")
                
                try:
                    request = requests.post('http://192.168.1.8:3080', json=payload)
                    print(request.text)
                except:
                    print("Base Deepstream doesn't seem to be online")
                    
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

def startReach():
    while True:
        reach()

Thread(target=startReach).start()

clients = {}

HOST = ''
BUFSIZ = 4096
ADDR = (HOST, 8080)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        SERVER.bind(ADDR)
        break
    except:
        subprocess.call(' sudo lsof -t -i tcp:8080 | xargs kill -9', shell = True)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=acceptConnections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()

