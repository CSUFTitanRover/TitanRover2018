from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import subprocess
from time import sleep
import smbus
import time


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


def handle_reading_pressure(client, addr, value):
    block = bus.read_word_data(addr, value)
    client.send(block)


def handle_activating_shock(client, addr, value):
    bus.write_i2c_block_data(int(addr), 0x00, StringToBytes(value))
    client.send('Successfully activated shock ', value)


def handle_client(client):
    while True:
        data = client.recv(4096)
        payload = data.split(',')
        addr = payload[0]
        value = payload[1]

        if payload[0] == '*':
            handle_reading_pressure(client, 30, value)
        if payload[0] == '+':
            handle_activating_shock(client, 30, value)


clients = {}

HOST = ''
PORT = '6789'
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
