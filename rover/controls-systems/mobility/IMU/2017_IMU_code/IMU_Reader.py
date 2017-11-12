import socket
import sys, time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 9016)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

while True:
    try:
    
        # Send data
        #message = 'This is the message.  It will be repeated.'
        #print >>sys.stderr, 'sending "%s"' % message
        #sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = 1#len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(6)
            amount_received += len(data)
            print >>sys.stderr, 'received "%s"' % data
    finally:
        time.sleep(0.000)
