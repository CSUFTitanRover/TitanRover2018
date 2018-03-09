import logging
import sys
import time
from deepstream import get, post
from Adafruit_BNO055 import BNO055

try:
    obj = {}
    post(obj, 'imu')
except:
    print("Not connected to deepstream")
magneticDeviation = 11

bno = BNO055.BNO055(busnum=2)
confMode = True

while True:
    try:
        if not bno.begin():
            print('The sensor is not connected')
            time.sleep(1)
            #raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
        else:
            break
    except:
        print('waiting for sensor...')

def magToTrue(h):
    global magneticDeviation
    if (h - magneticDeviation < 0):
        return (h + 360 - magneticDeviation)
    else:
        return h - magneticDeviation

bno.set_mode(0x00)
print("Entering Config Mode")
fileIn = open('calibrationData.txt','r')
data = fileIn.read().splitlines()
for i in range(len(data)):
    data[i] = int(data[i])
bno.set_calibration(data)
fileIn.close()

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')

try:
    while True:
        heading, roll, pitch = bno.read_euler()
	sys, gyro, accel, mag = bno.get_calibration_status()
	heading = magToTrue(heading)

	if (sys == 3 and gyro == 3 and accel == 3 and mag == 3 and confMode):
            bno.set_mode(0x0C)
	    print("Entering Nine Degrees of Freedom Fusion Mode")
            confMode = False
	print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
            heading, roll, pitch, sys, gyro, accel, mag))
        try:
            response = post({ "heading":heading, "roll":roll, "pitch":pitch, "sys":sys, "gyro":gyro, "accel":accel, "mag":mag }, 'imu')
        except:
            print("Cannot Post to Deepstream")
	response = None
	time.sleep(.03)
except:
    print("Error in try catch")
