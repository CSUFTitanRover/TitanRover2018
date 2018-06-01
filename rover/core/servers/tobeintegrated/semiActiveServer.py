from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import subprocess
from time import sleep
import smbus
import time

READ_PRESSURE = '9'
ACTIVATE_SHOCK_WHEEL_ONE = '1'
ACTIVATE_SHOCK_WHEEL_TWO = '2'
ACTIVATE_SHOCK_WHEEL_THREE = '3'
ACTIVATE_SHOCK_WHEEL_FOUR = '4'


# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)


def acceptConnections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client, )).start()


def StringToBytes(val):
    retVal = []
    for c in val:
        retVal.append(ord(c))
    return retVal


# def writeToBus(addr, deg, client):
#     #print(addr, type(int(addr)))
#     bus.write_i2c_block_data(int(addr), 0x00, StringToBytes(deg))
#     if deg[0] == '9':
#         block = bus.read_word_data(addr, 0)
#         client.send(block)
#     else:
#         client.send("Successful")


def handle_reading_pressure(client, addr, value):
    block = bus.read_word_data(addr, value)
    client.send(block)


def handle_activating_shock(client, addr, value):
    bus.write_i2c_block_data(int(addr), 0x00, StringToBytes(value))
    client.send('Successfully activated shock ', addr)


def handle_client(client):
    while True:
        data = client.recv(4096)
        payload = data.split(',')
        addr = payload[0]
        value = payload[1]

        if addr == READ_PRESSURE:
            handle_reading_pressure(client, addr, value)
        if addr in (ACTIVATE_SHOCK_WHEEL_ONE, ACTIVATE_SHOCK_WHEEL_TWO, ACTIVATE_SHOCK_WHEEL_THREE, ACTIVATE_SHOCK_WHEEL_FOUR):
            handle_activating_shock(client, addr, value)


clients = {}

HOST = ''
PORT = '9059'
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
while True:
    try:
        SERVER.bind(ADDR)
        break
    except:
        subprocess.call(
            ' sudo lsof -t -i tcp:9090 | xargs kill -9', shell=True)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=acceptConnections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
