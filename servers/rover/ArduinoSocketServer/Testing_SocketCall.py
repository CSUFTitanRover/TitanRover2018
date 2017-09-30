from socket import *
import time

#  Arduino address and connection info
address = ('192.168.1.177', 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

#  Command to Arduino
data = "run"
client_socket.sendto(data, address)

#need to find a clear buffer command to enable UDP 
data = "run"
client_socket.sendto(data, address)

exit()
