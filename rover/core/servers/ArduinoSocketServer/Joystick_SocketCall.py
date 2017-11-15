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
time.sleep(5)

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
#client_socket.settimeout(.5)

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
global modeWhenPaused
modeWhenPaused = ""

#global motor1, motor2, pauseInterval, pauseQuitInterval, modeWhenPause, motor_mult, arm1, arm2, joint5, joint6, joint7, mode

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
    except:
        print("Failed to send Stop Command")
        pass
    return;

#   This function changes the color of the LED on the Pi, based off of the current mode the rover is in
#   Green meaning BOTH Mobility and Arm are active
#   Blue meaning ONLY Mobility is active
#   Purple meaning ONLY Arm is active
#   Red meaning NEITHER Mobility or Arm is actice, we are in a paused state
#   Input: NONE
#   Output: NONE
def changeLedColor():
    if mode == "both":
        #LED Color = Green
        GPIO.output(greenLed,GPIO.HIGH)
        GPIO.output(redLed,GPIO.LOW)
        GPIO.output(blueLed,GPIO.LOW)
    elif mode == "mobility":
        #LED Color = Blue
        GPIO.output(greenLed, GPIO.LOW)
        GPIO.output(redLed, GPIO.LOW)
        GPIO.output(blueLed, GPIO.HIGH)
    elif mode == "arm":
        #LED Color = Purple
        GPIO.output(greenLed, GPIO.LOW)
        GPIO.output(redLed,GPIO.HIGH)
        GPIO.output(blueLed,GPIO.HIGH)
    elif mode == "pause":
        #LED Color = Red
        GPIO.output(redLed,GPIO.HIGH)
        GPIO.output(greenLed,GPIO.LOW)
        GPIO.output(blueLed,GPIO.LOW)

#   This function takes in a joystick and reads the values of each joystick Axis.
#   Based on the values of the joystick axis it sets the corresponding motor values
#   to be sent to the ESC.
#   Input: Joystick
#   Output: None
def checkJoystickMovement(currentJoystick):
    global motor1, motor2, pauseInterval, pauseQuitInterval, modeWhenPause, motor_mult, arm1, arm2, joint5, joint6, joint7, mode
    axes = currentJoystick.get_numaxes()

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
                    
#   This function takes in a joystick and cycles through all of the buttons to see if any are pushed.
#   If any are pushed it sets the corresponding command to the rover.
#   Input: Joystick
#   Output: None
#   List of Buttons and what they move (Logitech Wireless Controller).  
#   Button 1:   Joint 5.1   Rotate End Effector Left
#   Button 2:   Joint 4     Move Up
#   Button 3:   Joint 5.1   Rotate End Effector Right
#   Button 4:   Joint 4     Move Down
#   Button 5:   Joint 5.2   Close End Effector
#   Button 6:   Joint 5.2   Open End Effector
#   Button 7:   Decrease Motor Multiplier 
#   Button 8:   Increase Motor Multiplier
#   Button 9:   Pause/Unpause Rover commands
#   Button 10:  Switch between modes
#   Note: These button numbers are as they are on the controller.
#   In the for loop the buttons go from 0-9 not 1-10
def checkButtons(currentJoystick):
    global motor1, motor2, pauseInterval, pauseQuitInterval, modeWhenPause, motor_mult, arm1, arm2, joint5, joint6, joint7, mode, modeWhenPaused
    #Get the number of buttons on the joystick
    buttons = currentJoystick.get_numbuttons()

    # Cycle through every button set corresponding values depending on whether button is pushed or not.
    # Set the corresponding joint values if buttons 1-6
    # Adjust the motor multiplier if buttons 7,8
    # Pause/Unpause rover if Button 9
    # Switch modes if Button 10
    for i in range( buttons ):
        #Gets whether button is pushed or not (0 = not pushed, 1 = pushed)
        button = joystick.get_button( i )

        #If arm is active set joint values
        if mode == "both" or mode == "arm":
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
                
        # If mobility is active change multiplier if buttons are pushed
        if mode == "both" or mode == "mobility":
            # Motor Multiplier Commands
            if i == 6 and button == 1 and motor_mult > 0.31:
                motor_mult = motor_mult - .1
                print(motor_mult)
                
            if i == 7 and button == 1 and motor_mult < .9:
                motor_mult = motor_mult + .1
                print(motor_mult)

        # If Pause button is held down for atleast 3 seconds pause/unpause 
        if i == 9 and button == 1:
            if pauseQuitInterval == 0:
                pauseQuitInterval = datetime.now()
            elif (datetime.now() - pauseQuitInterval).seconds > 3:
                if mode != "pause":
                    print("Pausing Controls")

                    #Keeps mode when paused so we can return to the same mode
                    modeWhenPaused = mode
                    mode = "pause"
                    pauseQuitInterval = 0
                    stop()
                    #changeLedColor()
                elif mode == "pause":
                    print("Resuming Controls")
                    mode = modeWhenPaused
                    modeWhenPaused = ""
                    pauseQuitInterval = 0
                    #changeLedColor()
        elif i == 9 and button == 0 and pauseQuitInterval !=0:
            print("Reseting Pause Interval")
            pauseQuitInterval = 0
            
        #This button switches between different Modes
        #Green = Arm and Mobility
        #Blue = Mobility
        #Purple = Arm
        #Red = None (Paused)
        if i == 8 and button == 1:
            #print(pauseInterval)
            if pauseInterval == 0:
                pauseInterval = datetime.now()
            elif mode == "both":
                if (datetime.now() - pauseInterval).seconds > 3:
                    print("Switching to MOBILITY ONLY mode")
                    mode = "mobility"
                    #stop()
                    pauseInterval = 0
                    #LED color = Blue
                    #changeLedColor()
            elif mode == "mobility":
                if (datetime.now() - pauseInterval).seconds > 3:
                    print("Switcching to ARM ONLY mode")
                    #stop()
                    mode = "arm"
                    pauseInterval = 0
                    #LED Color = Purple
                    #changeLedColor()
            elif mode == "arm":
                if (datetime.now() - pauseInterval).seconds > 3:
                    print("Switching to BOTH mode")
                    #stop()
                    mode = "both"
                    pauseInterval = 0
                    #LED Color = Green
                    #changeLedColor()
        elif i == 8 and button == 0 and pauseInterval != 0:
            print("reseting Pause Interval")
            pauseInterval = 0
                
def checkHats(currentJoystick):
    global motor1, motor2, pauseInterval, pauseQuitInterval, modeWhenPause, motor_mult, arm1, arm2, joint5, joint6, joint7, mode
    hats = currentJoystick.get_numhats()

    if mode == "arm" or mode == "both": 
        for i in range( hats ):
            hat = joystick.get_hat( i )
            if hat[0] != 0:
                joint1 = hat[0]
            else:
                joint1 = 0
                    
#Depending on which mode we are in only the correct buttons will be checked
while(1):
    changeLedColor()
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

        checkJoystickMovement(joystick)
        checkButtons(joystick)
        checkHats(joystick)
        
    #  Command to Arduino
    if mode != 'pause':
        print 'Sending Command to Arduino'
        try:
            if mode == 'both':
                data = str(motor1) + ',' + str(motor2) + ',' + str(arm1) + ',' + str(arm2) + ',' + str(joint1) + ',' + str(joint5) + ',' + str(joint6) + ',' + str(joint7) + ',' + '0' + ',' + '0'
            elif mode == 'arm':
                data = '0' + ',' + '0' + ',' + str(arm1) + ',' + str(arm2) + ',' + str(joint1) + ',' + str(joint5) + ',' + str(joint6) + ',' + str(joint7) + ',' + '0' + ',' + '0'
            elif mode == 'mobility':
                data = str(motor1) + ',' + str(motor2) + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0'
            elif mode == 'pause':
                data = '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0' + ',' + '0'
            print (data)
            re_data, addr = client_socket.recvfrom(2048)
            print (re_data)
            
            if re_data == "ready":
                #data = str(motor1) + ',' + str(motor2) + ',' + str(arm1) + ',' + str(arm2) + ',' + str(joint1) + ',' + str(joint5) + ',' + str(joint6) + ',' + str(joint7) + ',' + '0' + ',' + '0'
                client_socket.sendto(data, address)
                print (data)
        except:
            print 'Failed'
            pass
    # Safety catch to force new values or shutdown old ones
    data = str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)
    joint1 = joint5 = joint6 = joint7 = motor1 = motor2 = arm1 = arm2   = 0
