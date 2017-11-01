from socket import *
from datetime import datetime
import time
import pygame

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

# Arduino address and connection info
address = ('192.168.1.177', 5000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

# Globals variables for data transmittion
global re_data
re_data = ""
global data
data = ""

# Globals for motor output
global motor2
motor2 = 0
global motor1
motor1 = 0
global pauseInterval
pauseInterval = 0
global pauseQuitInterval
pauseQuitInterval = 0
global pauseFull
pauseFull = False

# Global variable for motor throttle
global motor_mult
motor_mult = .5

# Globals variables for Arm and Joints
global arm1
arm1 = 0
global arm2
arm2 = 0
global joint5
joint5 = 0
global joint6
joint6 = 0
global joint7
joint7 = 0

# Initialize the connection to Arduino
client_socket.sendto('0,0', address)

def stop():
    try:
        re_data, addr = client_socket.recvfrom(2048)
        
        if re_data == "ready":
            data = str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)
            joint1 = joint5 = joint6 = joint7 = 0
            client_socket.sendto(data, address)
            print("Sent Stop Command")
    except:
        pass
    return;


while(1):
    for event in pygame.event.get(): # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print "Joystick button pressed."
        if event.type == pygame.JOYBUTTONUP:
            print "Joystick button released."
    
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # Sends Shutdown motor and arm commands if joystick is lost
    if joystick_count == 0:
        stop()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()    

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        hats = joystick.get_numhats()

        # Check for axes usage
        for i in range( axes ):
            axis = joystick.get_axis( i )
            if i == 1:
                motor1 = -int(127 * axis * motor_mult)
            if i == 0:  
                motor2 = int(127 * axis * motor_mult)
            if i == 2:  
                arm1 = int(127 * axis)
            if i == 3:  
                arm2 = int(127 * axis)
            
        buttons = joystick.get_numbuttons()

        # Check for button pushes
        for i in range( buttons ):
            button = joystick.get_button( i )

            # Joint commands
            if i == 1:
                joint5 = button
            elif i == 3 and joint5 == 0:
                joint5 = -button

            if i == 0:
                joint6 = button
            elif i == 2 and joint6 == 0:
                joint6 = -button    

            if i == 4:
                joint7 = button
            elif i == 5 and joint7 == 0:
                joint7 = -button

            # Motor Multiplier Commands
            if i == 6 and motor_mult < .9:
                if button == 1:
                    motor_mult = motor_mult + .1
                
            if i == 7 and motor_mult > .3:
                if button == 1:
                    motor_mult = motor_mult - .1
            # Script timed quit command
            if i == 8 and button == 1:
                    if pauseQuitInterval == 0:
                        pauseQuitInterval = datetime.now()
                    elif (datetime.now() - pauseQuitInterval).seconds > 3:
                        pygame.quit()
                        exit()

            # Joystick Pause command
            if i == 9 and button == 1:
                    if pauseInterval == 0:
                        pauseInterval = datetime.now()
                    elif (datetime.now() - pauseInterval).seconds > 3:
                        if pauseFull == False:
                            pauseFull = True
                            pauseInterval = 0
                            print "paused"
                            stop()
                        else:
                            print "unpaused"
                            pauseFull = False
                            pauseInterval = 0                
                
        for i in range( hats ):
            hat = joystick.get_hat( i )
            if hat[0] != 0:
                joint1 = hat[0]
            else:
                joint1 = 0
            
            
    #  Command to Arduino
    if not pauseFull:
        try:
            re_data, addr = client_socket.recvfrom(2048)
            
            if re_data == "ready":
                data = str(motor1) + ',' + str(motor2) + ',' + str(arm1) + ',' + str(arm2) + ',' + str(joint1) + ',' + str(joint5) + ',' + str(joint6) + ',' + str(joint7) + ',' + '0' + ',' + '0'
                client_socket.sendto(data, address)
                print (data)
        except:
            pass
    # Safety catch to force new values or shutdown old ones
    data = str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)
    joint1 = joint5 = joint6 = joint7 = 0
