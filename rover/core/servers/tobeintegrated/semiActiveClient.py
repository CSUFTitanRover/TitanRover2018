# Python TCP Client
import socket


def connect():
    host = "192.168.1.2"
    port = 6789
    BUFFER_SIZE = 4096

    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect((host, port))

    while True:
        try:
            MESSAGE = raw_input("Enter : ")
            Client.send(MESSAGE)
            data = Client.recv(BUFFER_SIZE)
            print(data)
        except:
            Client.close()
            break
        print(" Client received data:", data)


connect()
