
from socket import *
import time
import pygame

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

#  Arduino address and connection info
address = ('192.168.1.177', 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

#Globals for motor output
global re_data
re_data = ""
global motor2
motor2 = 0
global motor1
motor1 = 0

#initialize the connection to Arduino
client_socket.sendto("0,0", address)


while(1):
    for event in pygame.event.get(): # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()    

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()

        for i in range( axes ):
            axis = joystick.get_axis( i )
            if i == 1:
                motor1 = -127 * axis
            if i == 0:  
                motor2 = 127 * axis
            
        buttons = joystick.get_numbuttons()

        for i in range( buttons ):
            button = joystick.get_button( i )

        #for i in range( hats ):
        #    hat = joystick.get_hat( i )
            
    #  Command to Arduino
    try:
        re_data, addr = client_socket.recvfrom(2048)
    except:
        pass
    if re_data == "ready":
        print "sending"
        data = str(motor1) + ',' + str(motor2)
        client_socket.sendto(data, address)
    data = str(0) + ',' + str(0)
    
exit(0)
