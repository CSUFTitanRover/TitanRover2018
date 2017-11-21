#Written by Brandon Hawkinson and Timothy Parks
#atlasCore is an interactive shell tool to run, debug and change states of the rover from multiple input sources.

import socket
import time
import sys

def Main():
    isConnected = False
    host = "127.0.0.1"
    port = 5000
    count = 0 #counter int to keep track of how many 
    m = "" #message recieved back from the server
    s = socket.socket() #socket object

    print("Welcome to atlasCore, attempting to establish a connection to the core...")
    while isConnected == False:        
        try:
            s.connect((host, port))
            isConnected = True
        except socket.error:
            print("Connection not established... " + str(count) + " times")
            time.sleep(.5)
            
            if count % 20 == 0 and count != 0:
                print("Failed to connect to core... try again? (y -> yes)")
                m = input(" -> ")
                if m != "y":
                    break
                    print("exiting...")

            count += 1

        if isConnected == True:
            print("Connection to core established... took " + str(count) + " times")
            print("Type \"Help\" for a list of commands \n Type \"r\" to restart the connection \n Type \"q\" to quit the program")
            count = 0
                    
            while m != "r" and m != "q":
                m = input(" -> ")
                if m.lower() == "r":
                    s.close()
                    isConnected = False
                    print("Restarting the connection...")
                elif sm.lower() == "q":
                    s.close()
                    break
                elif m.lower() == "help"
                else:
                    s.send(message.encode())
                    d = s.recv(1024).decode()

                    print('Command executed: ' + d)


if __name__ == '__main__':
    Main()