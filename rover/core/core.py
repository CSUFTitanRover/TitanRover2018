#Written by Brandon Hawkinson and Timothy Parks
#core is a server that runs at start up to connect to the UI, this will automate starting processes when we recieve a UI command.

import socket
import time
import logging
import subprocess

version = "0.0.1"

modeFiles = dict([
    ("manual" , "\process-managers\manualProcessManager.py"),
    ("remote" , "\process-managers\\remoteProcessManager.py"), #requires escape
    ("autonomous" , "\process-managers\\autonomousProcessManager.py"), #requires escape
    ("science" , "\process-managers\scienceProcessManager.py")
])
 
def Main():
    t = time.strftime("%m%d%Y-%H%M%S")
    logging.basicConfig(filename='debug\coreDump_' + t + '.log',level=logging.DEBUG)
    logging.info('Started log at ' + t)

    command = ""
    host = "127.0.0.1"
    port = 5000
     
    s = socket.socket()
    s.bind((host,port))
    logging.info("Bound socket to the host: " + host + ", on port: " + port)

    while command != "restart":
    
     
    s.listen(1)
    conn, addr = s.accept()
    logging.warning("Connection from: " + str(addr))
    while True:
            d = conn.recv(1024).decode()
            if not d:
                    break
            logging.warning("from connected  user: " + str(d))
            if d == "getVersion": 
                d = str(version)
                logging.warning("sending: " + str(d))
                conn.send(d.encode())
            else:
                d = str(d).upper()
                logging.warning("sending: " + str(d))
                conn.send(d.encode())
    conn.close()

    t = time.strftime("%m%d%Y-%H%M%S")
    logging.info('Stopped log at ' + t)
     
if __name__ == '__main__':
    Main()