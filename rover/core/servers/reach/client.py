# Python TCP Client
import socket 
import pickle

class Gnss:

    def connect(self):
        host = "localhost" 
        port = 9090
        BUFFER_SIZE = 4096 

        Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        Client.connect((host, port))

        while True:
            try:
                MESSAGE = raw_input("Enter : ")
                Client.send(MESSAGE)     
                data = Client.recv(BUFFER_SIZE)
                #data = data.split(',')
                data = pickle.loads(data)
            except:
                Client.close()
                break
            print(" Client A received data:", data)


# Example on How to import this Module
'''
from client import Gnss
gps = Gnss()
gps.connect()
'''