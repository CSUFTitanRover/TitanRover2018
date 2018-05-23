from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread 
import pickle
import subprocess
from time import sleep
from deepstream import post

global currentPoints
global previousPoints
currentPoints = []
previousPoints = []


def acceptConnections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client, )).start()


def handle_client(client):
    global currentPoints
    while True : 
        data = client.recv(4096) 
        print("Server received data:", data)
        print(type(data))
        if data[0] == '0':
            currentPoints = []
            client.send(pickle.dumps(currentPoints))
            print("Empty List Successful")

        elif data[0] == '1':
            addPoint(data)
            client.send(pickle.dumps(currentPoints))
            print("Add Point Successful")

        elif data[0] == '2':
            deletePoints(data)
            client.send(pickle.dumps(currentPoints))
            print("Delete Point Successful")

        elif data[0] == '3':
            client.send(readTopPoint(data))
            print("Top Read Successful")

        elif data[0] == '4':
            client.send(pickle.dumps(currentPoints))
            print("ReadAll Successful")

        else:
            client.send("Invalid Input")
                        

        #MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
        #conn.send(MESSAGE)  # echo 

def addPoint(MESSAGE):
    global currentPoints
    #print("into addpoint")
    points = MESSAGE.split(",")

    #print("The points is ", points)
    for x in range(1, len(points), 2):
        temp = (points[x],points[x+1]) 
        currentPoints.append(temp)


def deletePoints(MESSAGE):
    global currentPoints
    global previousPoints
    #print("into deletepoints")
    points = MESSAGE.split(",")

    #print("The points is ", points)
    #print("size of point is ", len(points))
    if len(points) == 3:
        temp = (points[1],points[2])
        previousPoints.append(temp)
        del currentPoints[currentPoints.index(temp)]
    elif len(currentPoints) != 0:
        previousPoints.append(currentPoints[-1])
        del currentPoints[-1]
    

def readTopPoint(MESSAGE):
    global currentPoints
    #print("into readtoppoint")
    #temp = ','.join(currentPoints[-1])
    if currentPoints:
        temp = pickle.dumps(currentPoints[-1])
    else:
        temp = pickle.dumps(currentPoints)
    return temp
    
def sendToBaseStation():
    global currentPoints
    global previousPoints
    while True:
        try:
            post({ 'cp' : currentPoints}, "currentPoints")
            post({ 'pp' : previousPoints}, "previousPoints")
            print("Successful Post")
        except:
            print("Cannot Send to HomeBase")
        sleep(5)


Thread(target=sendToBaseStation).start()

clients = {}

HOST = ''
PORT = 9090
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
while True:
    try:
        SERVER.bind(ADDR)
        break
    except:
        subprocess.call(' sudo lsof -t -i tcp:9090 | xargs kill -9', shell = True)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=acceptConnections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    Thread(target=sendToBaseStation).start()
SERVER.close()