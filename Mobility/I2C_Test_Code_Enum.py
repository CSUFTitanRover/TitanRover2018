import smbus
import time
from enum import Enum

# Sets enumerators and their values
class commands(Enum):
    UNKNOWN_COMMAND = 0
    LED = 1
    SERVO = 2

# Initializes bus to smbus
bus = smbus.SMBus(1)

# This is the slave address we setup in the Arduino Program
address = 0x04

def writeCommand(cmd):
    # Converts any capital letters to lower case
    cmd = cmd.lower()
    # Writes the value that is equivalent to the enumerator to the bus
    if cmd == 'led':
        bus.write_byte(address, commands.LED.value)
    elif cmd == 'servo':
        bus.write_byte(address, commands.SERVO.value)
    # If user input is not a valid command, does not write anything to the bus
    return -1

def readCommand():
    # Reads value that the Arduino passes back
    cmd = bus.read_byte(address)
    return cmd

while True:
    # Stores user input as var
    var = input("Enter a valid command {led, servo}: ")
    if not var:
        continue
    # Function call to send Arduino a command based on user input
    writeCommand(var)
    print("RPI: Hi Arduino, I sent you", var)
    # Retrieve value that was received by the Arduino
    cmd = readCommand()
    print("Arduino: Hey RPI, I received", commands(cmd))
