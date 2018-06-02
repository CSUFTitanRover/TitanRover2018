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
            message1 = '30,91'
            message2 = '30,92'
            message3 = '30,93'
            message4 = '30,94'

            Client.send(message1)
            data1 = Client.recv(BUFFER_SIZE)
            print(f'Front Left pressure: {data1}')

            Client.send(message2)
            data2 = Client.recv(BUFFER_SIZE)
            print(f'Front Right pressure: {data2}')

            Client.send(message3)
            data3 = Client.recv(BUFFER_SIZE)
            print(f'Back Left pressure: {data3}')

            Client.send(message4)
            data4 = Client.recv(BUFFER_SIZE)
            print(f'Back Right pressure: {data4}')

            print('-------------------')
        except:
            Client.close()
            break


connect()
