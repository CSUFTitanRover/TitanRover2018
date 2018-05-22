import socket
from binascii import hexlify, unhexlify, a2b_hex, b2a_hex, b2a_qp, a2b_qp
from struct import *
from time import sleep

#USE PORT_NO = 7080 for websockets to send data

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
    print('sending..')
    lidarSocket.send(g)
    print('receiving..')
    d = lidarSocket.recv(4096)
    #print(d)
    data = d.split(" ")
    dataPoints = int("0x" + str(data[25]), 16)
    print(dataPoints)

    for x in range(26, 26 + dataPoints, 1):
        distance.append(data[x])
    print("\n\nHEX VALUE -------------------------------------------")
    print(distance)

    for x in range(len(distance)):
        distance[x] = (int("0x" + str(distance[x]), 16), degree)
        #if distance[x] < 1800 and distance[x] > 600:
            #print("distance is less : " + str(distance[x]) + " at degree" + str(degree) + " position : " + str(x))
            #sleep(.1)
        degree -= 0.5

    print("\n\nDECIMAL VALUE -------------------------------------------")
    print(distance)

    sleep(.05)

