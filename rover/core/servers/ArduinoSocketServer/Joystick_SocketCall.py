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

#Globals variables for data transmittion
global re_data
re_data = ""
global data
data = ""

#Globals for motor output
global motor2
motor2 = 0
global motor1
motor1 = 0

#Global variable for motor throttle
global motor_mult
motor_mult = .5

#Globals variables for Arm and Joints
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

#initialize the connection to Arduino
client_socket.sendto('0,0', address)


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
        try:
            re_data, addr = client_socket.recvfrom(2048)
            if re_data == "ready":
                data = str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)
                client_socket.sendto(data, address)
        except:
            pass

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
            #print("In Button")

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

            if i == 6 and motor_mult < .9:
                if button == 1:
                    motor_mult = motor_mult + .1
                
            if i == 7 and motor_mult > .3:
                if button == 1:
                    motor_mult = motor_mult - .1

            if i == 9 and button == 1:
                pygame.quit()
                
        for i in range( hats ):
            hat = joystick.get_hat( i )
     #       print("In Hat")
            if hat[0] != 0:
                joint1 = hat[0]
            else:
                joint1 = 0
            
            
    #  Command to Arduino
    try:
        re_data, addr = client_socket.recvfrom(2048)
        if re_data == "ready":
            #print "sending"
            data = str(motor1) + ',' + str(motor2) + ',' + str(arm1) + ',' + str(arm2) + ',' + str(joint1) + ',' + str(joint5) + ',' + str(joint6) + ',' + str(joint7) + ',' + '0' + ',' + '0'
            client_socket.sendto(data, address)
            print (data)
            #print("In try")
    except:
        pass
    #print("After Try/Catch")
    # Safety catch to force new values or shutdown old ones
    data = str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)
    joint1 = joint5 = joint6 = joint7 = 0
pygame.quit()
