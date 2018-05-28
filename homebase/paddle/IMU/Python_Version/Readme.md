
File IMU_Acc_Mag_Gyro.py
==============================================================================================================================

This program will read the IMU registers and provide heading, pitch, roll angles.  Written to function with the Adafruit 10-DOF 
IMU Breakout board which has the following chips:

1. LSM303DLHC - Accelerometer Compass
2. L3DG20H - Gyroscope
3. BMP180 - Barometric/Temperature sensor

This script will provide all axis, temp, and pressure values to the Rover system when 
the process is called upon.  

Communication: I2C

==============================================================================================================================

Version:  1.0 
=============
Date:  12/29/16

- Provides output for all axis information.  Software bug for chip orientation if flipped over.

Version:   1.1
=============
Date:  1/03/16

- Commented out unused output for Rover system.  
- Added test.js which simulates the reading of values from IMU_Acc_Mag_Gyro.py process
	- Software bug exists in transfer of first value between Python Script and Test.js
- Disabled looping functions to save process cycles on Raspberry Pi.

Version:   1.2
=============
Date:   1/05/16

- Combined seperated functions and cleaned up code

BEFORE

	def readACCx():
		.....( 8 lines of code )
	def readACCy():
		.....( 8 lines of duplicate code )
	def readACCz():
		.....( 8 lines of duplicate code )

AFTER

	def readACCAxis(axis):
		reg = LSM303_ACCEL_OUT_X_L_A
		if axis == 'x':
			acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg) 
			acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 1) 
		elif axis == 'y':
			acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 2)
			acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 3)
		else: #axis == 'z':
			acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 4)
			acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 5)
		acc_combined = (acc_l | acc_h <<8)
		return acc_combined  if acc_combined < 32768 else acc_combined - 65536
		

- Timing Analysis clocks the test.js start to receive @ 105ms


Bugs:
=============
>test.js still has a issue with first value return.  Chip flip will cause a crash if happens while being read from.


Future Plans:
=============

>Need to add initializations of IMU to start up files in linux.  Each time process starts the chip is reinit. causing possible delay in process timing.
