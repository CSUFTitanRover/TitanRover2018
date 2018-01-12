import socket
from time import sleep
import subprocess
import serial

#i = 1

def startListening():
    while True:
        try:
            ser = serial.Serial('/dev/tty-emlid', baudrate=115200)
            break
        except:
            print("Not Connected to the Reach on /dev/ttyACM*")
            sleep(1)

            #counter = 0
            #pid = subprocess.call(["sudo", "lsof", "-t", "-i", "tcp:9000"])
            #while counter < 5:
                #subprocess.call(' sudo lsof -t -i tcp:9000 | xargs kill -9', shell = True)
                #counter += 1
            
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 9000))
    s.listen(5)

    print("Waiting For Connection")

    while True:
        try:
            conn, address = s.accept()
            print("Connection from", address)
            break
        except:
            print("ERROR CONNECTING")
            sleep(1)

    while True:
        try:
            ser = serial.Serial('/dev/tty-emlid', baudrate=115200)
            data = conn.recv(1024)
            ser.write(data)
            print("Sending Data Successfully")
        except:
            #i = 0
            print("Connection Terminated")
            break
        '''
        except:
            print("Not Connected to the Reach on /dev/ttyACM*")
            sleep(1)
            #if i is 0:
            #subprocess.call(["python", "socketServer.py"])
            #i = 1
        '''


while True:
    try:
        startListening()
    except:
        subprocess.call(' sudo lsof -t -i tcp:9000 | xargs kill -9', shell = True)
