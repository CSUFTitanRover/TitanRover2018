import smbus
import time
from enum import Enum

class commands(Enum):
    UNKNOWN_COMMAND = 0
    LED = 1
    SERVO = 2

# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    #bus.write_byte(address,int(value, 24))
    value = value.lower()
    if value == 'led':
        bus.write_byte(address, commands.LED.value)
    elif value == 'servo':
        bus.write_byte(address, commands.SERVO.value)
    else:
        bus.write_byte(address, commands.UNKNOWN_COMMAND.value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

while True:
    var = input("Enter a valid command {led, servo}: ")
    
    if not var:
        continue
    writeNumber(var)
    print("RPI: Hi Arduino, I sent you ", var)
    # sleep one second
    time.sleep(1)

    number = readNumber()
    print("Arduino: Hey RPI, I received a digit ", commands(number))
import smbus
import time

# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

