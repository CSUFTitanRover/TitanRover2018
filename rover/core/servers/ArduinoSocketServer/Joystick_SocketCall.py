#!/bin/sh

### BEGIN INIT INFO
# Provides:             RoverMobilityServer
# Required-Start:       $remote_fs $network $syslog
# Required_Stop:        $remote_fs $syslog
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    Simple script to start a program at boot
# Description:          Rover Mobility Server
### END INIT INFO

from socket import *
from datetime import datetime
import time
import pygame
import RPi.GPIO as GPIO

# WAIT FOR STUFF
time.sleep(15)

#LED Signals for status 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
redLed = 18
greenLed = 23
blueLed = 24
GPIO.setup(redLed, GPIO.OUT) #Red LED
GPIO.setup(greenLed, GPIO.OUT) #Green LED
GPIO.setup(blueLed, GPIO.OUT) #Blue LED


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

global mode
mode = "both"

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
            GPIO.output(redLed,GPIO.HIGH)
            GPIO.output(greenLed,GPIO.LOW)
            GPIO.output(blueLed,GPIO.LOW)
    except:
        print("Failed to send Stop Command")
        pass
    return;

GPIO.output(greenLed,GPIO.HIGH)
GPIO.output(redLed,GPIO.LOW)
GPIO.output(blueLed,GPIO.LOW)

#Depending on which mode we are in only the correct buttons will be checked
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
            if mode == "mobility" or mode == "both":
                if i == 1:
                    motor1 = -int(127 * axis * motor_mult)
                if i == 0:  
                    motor2 = int(127 * axis * motor_mult)
            if mode == "arm" or mode == "both":
                if i == 2:  
                    arm1 = int(127 * axis)
                if i == 3:  
                    arm2 = int(127 * axis)
                    
            

            
        buttons = joystick.get_numbuttons()

        # Check for button pushes
        for i in range( buttons ):
            button = joystick.get_button( i )
            if (mode == "both" or mode == "arm"):
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

            if (mode == "both" or mode == "mobility"):
                # Motor Multiplier Commands
                if i == 6 and button == 1 and motor_mult > 0.31:
                    #if button == 1:
                    motor_mult = motor_mult - .1
                    print(motor_mult)
                    
                if i == 7 and button == 1 and motor_mult < .9:
                    #if button == 1:
                    motor_mult = motor_mult + .1
                    print(motor_mult)
        # Script timed quit command
            if i == 8 and button == 1:
                if pauseQuitInterval == 0:
                    pauseQuitInterval = datetime.now()
                elif (datetime.now() - pauseQuitInterval).seconds > 3:
                    GPIO.output(greenLed,GPIO.LOW)
                    GPIO.output(redLed,GPIO.LOW)
                    GPIO.output(blueLed,GPIO.LOW)
                    pygame.quit()
                    exit()
            #This button switches between different Modes
            #Green = Arm and Mobility
            #Blue = Mobility
            #Yellow = Arm
            #Red = None (Paused)
            if i == 9 and button == 1:
                #print(pauseInterval)
                if pauseInterval == 0:
                    pauseInterval = datetime.now()
                elif mode == "both":
                    if (datetime.now() - pauseInterval).seconds > 3:
                        print("Switching to MOBILITY ONLY mode")
                        mode = "mobility"
                        pauseInterval = 0
                        #LED color = Blue
                        GPIO.output(greenLed, GPIO.LOW)
                        GPIO.output(redLed,GPIO.LOW)
                        GPIO.output(blueLed,GPIO.HIGH)
                        
                elif mode == "mobility":
                    if (datetime.now() - pauseInterval).seconds > 3:
                        print("Switcching to ARM ONLY mode")
                        mode = "arm"
                        pauseInterval = 0
                        #LED Color = Yellow?
                        GPIO.output(greenLed, GPIO.HIGH)
                        GPIO.output(redLed,GPIO.HIGH)
                        GPIO.output(blueLed,GPIO.LOW)
                elif mode == "arm":
                    if (datetime.now() - pauseInterval).seconds > 3:
                        print("Pausing Controls")
                        mode = "pause"
                        pauseInterval = 0
                        stop()
                        #LED Color = RED
                elif mode == "pause":
                    if (datetime.now() - pauseInterval).seconds > 3:
                        print("Switching to BOTH mode")
                        mode = "both"
                        pauseInterval = 0
                        GPIO.output(greenLed, GPIO.HIGH)
                        GPIO.output(redLed,GPIO.LOW)
                        GPIO.output(blueLed,GPIO.LOW)
            elif i == 9 and button == 0 and pauseInterval != 0:
                print("reseting Pause Interval")
                pauseInterval = 0
        if mode == "arm" or mode == "both": 
            for i in range( hats ):
                hat = joystick.get_hat( i )
                if hat[0] != 0:
                    joint1 = hat[0]
                else:
                    joint1 = 0
                    
##            # Joystick Pause command
##            #if i == 9 and button == 1:
##            #    if pauseInterval == 0:
##            #        print("getting pause interval start")
##            #        pauseInterval = datetime.now()
##            #    elif (datetime.now() - pauseInterval).seconds > 3:
##            #        print("Longer than 3 seconds")
##                    if pauseFull == False:
##                        pauseFull = True
##                        pauseInterval = 0
##                        print "paused"
##                        stop()
##                    elif pauseFull == True:
##                        print "unpaused"
##                        pauseFull = False
##                        pauseInterval = 0
##                        GPIO.output(greenLed,GPIO.HIGH)
##                        GPIO.output(redLed,GPIO.LOW)
##                        GPIO.output(blueLed,GPIO.LOW)
            
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
