from socket import *
import time

#  Arduino address and connection info
address = ('192.168.1.177', 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

#Globals for motor output
global re_data
re_data = ""
global motor2
motor2 = 256
global motor1
motor1 = 0

client_socket.sendto("0,0", address)
while(1):
    print "running"
    if motor1 == 256:
        print "if"
        motor1 = 127
        motor2 = 127
        data = str(motor1) + ',' + str(motor2)
        client_socket.sendto(data, address)
        exit(0)
    
    motor1 += 1
    motor2 -= 1
    
    #  Command to Arduino
    try:
        
        re_data, addr = client_socket.recvfrom(2048)
    except:
        pass
    if re_data == "ready":
        print "sending"
        data = str(motor1) + ',' + str(motor2)
        client_socket.sendto(data, address)

exit(0)
