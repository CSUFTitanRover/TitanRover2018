import serial
import struct
ser = serial.Serial('/dev/ttyACM1', 9600, timeout=None)# device type may change -> needs immediate addressing
mystruct = struct.pack("i", yourinthere)
ser.write(mystruct)
