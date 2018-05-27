# Python TCP Client
import socket 


def connect():
    host = "localhost" 
    port = 9080
    BUFFER_SIZE = 4096 

    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    Client.connect((host, port))

    while True:
        try:
            MESSAGE = raw_input("Enter : ")
            Client.send(MESSAGE)     
            data = Client.recv(BUFFER_SIZE)
            #data = data.split(',')
            #data = pickle.loads(data)
        except:
            Client.close()
            break
        print(" Client received data:", data)


connect()
