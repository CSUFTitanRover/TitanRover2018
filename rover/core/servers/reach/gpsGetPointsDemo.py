# Python TCP Client
import socket 
from time import sleep


def connect():
    host = "192.168.1.2" 
    port = 8080
    BUFFER_SIZE = 4096 

    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    Client.connect((host, port))

    while True:
        try:
            #MESSAGE = raw_input("Enter : ")
            #Client.send(MESSAGE)     
            data = Client.recv(BUFFER_SIZE)
            print(" Client received data:", data)
            #data = data.split(',')
            #data = pickle.loads(data)
        except:
            Client.close()
            break

connect()
