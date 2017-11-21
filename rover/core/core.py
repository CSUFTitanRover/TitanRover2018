#Written by Brandon Hawkinson and Timothy Parks
#core is a server that runs at start up to connect to the UI, this will automate starting processes when we recieve a UI command.

import socket
import time
import logging
import subprocess
 
def Main():
    t = time.strftime("%m%d%Y-%H%M%S")
    logging.basicConfig(filename='debug\coreDump_' + t + '.log',level=logging.DEBUG)
    logging.info('Started log at ' + t)

    host = "127.0.0.1"
    port = 5000
     
    s = socket.socket()
    s.bind((host,port))
     
    s.listen(1)
    conn, addr = s.accept()
    logging.warning("Connection from: " + str(addr))
    while True:
            d = conn.recv(1024).decode()
            if not d:
                    break
            logging.warning("from connected  user: " + str(d))
             
            d = str(d).upper()
            logging.warning("sending: " + str(d))
            conn.send(d.encode())
             
    conn.close()

    t = time.strftime("%m%d%Y-%H%M%S")
    logging.info('Stopped log at ' + t)
     
if __name__ == '__main__':
    Main()