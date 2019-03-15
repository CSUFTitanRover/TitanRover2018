# Python TCP Client
import socket 
import pickle
from time import sleep


host = "192.168.1.120" 
port = 7080
BUFFER_SIZE = 8192 

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
Client.connect((host, port))

while True:
    try:
        MESSAGE = raw_input("Enter : ")
        Client.send(MESSAGE)     
        data = Client.recv(BUFFER_SIZE)
        #data = data.split(',')
        print(type(data))
        data = pickle.loads(data)
    except:
        Client.close()
        break
    print(" Client A received data: \n", data)
    sleep(0.05)

