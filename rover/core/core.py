#Written by Brandon Hawkinson and Timothy Parks
#core is a server that runs at start up to connect to the UI, this will automate starting processes when we recieve a UI command.

import socket
import time
import logging
import subprocess

version = "0.0.1"

modeFiles = dict([
    ("manual" , "./process-managers/manualProcessManager.py"),
    ("remote" , "./process-managers/remoteProcessManager.py"), #requires escape
    ("autonomy" , "./process-managers/autonomyProcessManager.py"), #requires escape
    ("science" , "./process-managers/scienceProcessManager.py")
])
 
def Main():
    t = time.strftime("%m%d%Y-%H%M%S")
    logging.basicConfig(filename='debug/coreDump_' + t + '.log',filemode='w', level=logging.DEBUG)
    logging.info('Started log at ' + t)

    running = True
    command = ""
    host = "127.0.0.1"
    port = 5000
     
    s = socket.socket()
    s.bind((host,port))
    logging.info("Bound socket to the host: " + str(host) + ", on port: " + str(port))

    while running == True:
        s.listen(1)
        conn, addr = s.accept()
        logging.warning("Connection from: " + str(addr))
        cCommand = True
        while True:
                if cCommand == True:
                    command = conn.recv(1024).decode()
                if not command:
                        break
                logging.warning("from connected  user: " + str(command))
                if command == "getVersion": 
                    command = str(version)
                    logging.warning("sending: " + str(command))
                    conn.send(command.encode())

                elif command == "restartCore":
                    conn.close()
                    running = False
                    break

                elif command == "setModeManual" or command == "setModeRemote" or command == "setModeAutonomy" or command == "setModeScience" or command == "setModeDefault" :
                    if command == "setModeManual" :
                        cval = "manual"
                    elif command == "setModeRemote" :
                        cval = "remote"
                    elif command == "setModeAutonomy" :
                        cval = "autonomy"
                    elif command == "setModeScience" :
                        cval = "science"
                    else :
                        if cConnect == True :
                            cval = "manual"
                        else :
                            cval = "remote"
                    command = str(command).upper()
                    logging.warning("sending: " + str(command))
                    conn.send(command.encode())
                    subprocess.call('python3 ' + str(modeFiles.get(cval)), shell = True)

                else:
                    command = str(command).upper()
                    logging.warning("sending: " + str(command))
                    conn.send(command.encode())
        conn.close()

    t = time.strftime("%m%d%Y-%H%M%S")
    logging.info('Stopped log at ' + t)
     
if __name__ == '__main__':
    Main()