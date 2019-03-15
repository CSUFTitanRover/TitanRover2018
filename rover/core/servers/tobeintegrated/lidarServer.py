import socket
#from binascii import hexlify, unhexlify, a2b_hex, b2a_hex, b2a_qp, a2b_qp
from struct import *
from time import sleep
import pickle
import subprocess
from threading import Thread

global obsData, obs
obsData = []
obs = []

def getLidarData():
    global obsData, obs

    lidarAddress = ('192.168.1.25', 2111)
    lidarSocket = socket.create_connection(lidarAddress)

    g = bytearray(b' \x02\x73\x52\x4e\x20\x4c\x4d\x44\x73\x63\x61\x6e\x64\x61\x74\x61\x03')

    print(g)
    """
        in order to get one thing of data at a time, send:
            sRN LMDscandata
        in order to get multiple messages send:
            sRN LMDscandata 1
    """

    lidarSocket.send(g)

    while True:
        degree = 90
        distance = []
        obsData = []
        obs = []
        print('sending..')
        lidarSocket.send(g)
        print('receiving..')
        d = lidarSocket.recv(8192)
        #print(d)
        data = d.split(" ")
        dataPoints = int("0x" + str(data[25]), 16)
        #print(dataPoints)

        if dataPoints == 361:
            for x in range(26, 26 + dataPoints, 1):
                distance.append(data[x])
            #print("\n\nHEX VALUE -------------------------------------------")
            #print(distance)
            #print(len(distance))
            #print(type(distance[100]))


            for z in range(len(distance)):
                obsData.append((int("0x" + str(distance[z]), 16), degree))
                if obsData[z][0] < 1800 and obsData[z][0] > 600:
                    #print(obsData[z])
                    obs.append(obsData[z])
                degree -= 0.5

            print("Scan Successful")
            #print("\n\nDECIMAL VALUE -------------------------------------------")
            #print(obs)
            #print(len(obsData))
        else:
            continue

        sleep(0.05)


def sendLidarData():
    #USE PORT_NO = 7080 for websockets to send data
    global obsData, obs
    
    ADDR = ('', 7080)
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            SERVER.bind(ADDR)
            SERVER.listen(2)
            break
        except:
            subprocess.call(' sudo lsof -t -i tcp:9090 | xargs kill -9', shell = True)
            sleep(10)

    while True:
        try:
            client, client_address = SERVER.accept()
            print("%s:%s has connected." % client_address)
            break
        except:
            print("waiting for client to connect")
            sleep(5)
    

    while True:
        cmd = client.recv(512)
        #print("Server received data: ", cmd)
        #print(type(cmd))
        if cmd == 'ready':
            print("sending Data")
            client.send(pickle.dumps(obs))
            #client.send(pickle.dumps(obsData))
            print("Send Successful")
        else:
            client.send(pickle.dumps([(0,0)]))
            print("Null Send Successful")


Thread(target=getLidarData).start()
Thread(target=sendLidarData).start()
