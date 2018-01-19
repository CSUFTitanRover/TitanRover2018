####################################################################################
#
#       Program dependancies the IMU must circuit must be placed either facing up
#       or facing down for accurate initialization process.  Depending on up/down
#       several lines of codes need to be commented out or used.  These sections
#       of code are titled:
#                       ##########Direction Requirement###########
#       for the purposes of this project which used the Adafruit 10-DOF the unit
#       is considered upside down if the IC's on the IMU are facing the direction
#       of the earth.  Right side up is IC's facing the sky.
#
####################################################################################


import sys

import smbus
import time
import math
from LSM303_U import *
from L3GD20_GYRO import *
import datetime
bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant
try:
	MAGNETIC_DECLINATION=float(sys.argv[1])

except:
	print(sys.argv[1])
	print("Missing Arguments: Required Magnetic Declination")
	exit(0)

#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
x_bias = y_bias = 0.0
XP_00 = XP_01 = XP_10 = XP_11 = 0.0
YP_00 = YP_01 = YP_10 = YP_11 = 0.0
KFangleX = KFangleY = 0.0

def kalmanFilterY ( accAngle, gyroRate, DT):
	y=0.0
	S=0.0

	global KFangleY
	global Q_angle
	global Q_gyro
	global y_bias
	global YP_00
	global YP_01
	global YP_10
	global YP_11

	KFangleY = KFangleY + DT * (gyroRate - y_bias)

	YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
	YP_01 = YP_01 + ( - DT * YP_11 )
	YP_10 = YP_10 + ( - DT * YP_11 )
	YP_11 = YP_11 + ( + Q_gyro * DT )

	y = accAngle - KFangleY
	S = YP_00 + R_angle
	K_0 = YP_00 / S
	K_1 = YP_10 / S
	
	KFangleY = KFangleY + ( K_0 * y )
	y_bias = y_bias + ( K_1 * y )
	
	YP_00 = YP_00 - ( K_0 * YP_00 )
	YP_01 = YP_01 - ( K_0 * YP_01 )
	YP_10 = YP_10 - ( K_1 * YP_00 )
	YP_11 = YP_11 - ( K_1 * YP_01 )
	
	return KFangleY

def kalmanFilterX ( accAngle, gyroRate, DT):
	x=0.0
	S=0.0

	global KFangleX
	global Q_angle
	global Q_gyro
	global x_bias
	global XP_00
	global XP_01
	global XP_10
	global XP_11


	KFangleX = KFangleX + DT * (gyroRate - x_bias)

	XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
	XP_01 = XP_01 + ( - DT * XP_11 )
	XP_10 = XP_10 + ( - DT * XP_11 )
	XP_11 = XP_11 + ( + Q_gyro * DT )

	x = accAngle - KFangleX
	S = XP_00 + R_angle
	K_0 = XP_00 / S
	K_1 = XP_10 / S
	
	KFangleX = KFangleX + ( K_0 * x )
	x_bias = x_bias + ( K_1 * x )
	
	XP_00 = XP_00 - ( K_0 * XP_00 )
	XP_01 = XP_01 - ( K_0 * XP_01 )
	XP_10 = XP_10 - ( K_1 * XP_00 )
	XP_11 = XP_11 - ( K_1 * XP_01 )
	
	return KFangleX

'''
def writeRegisterAxis(Address, register, value):
	bus.write_byte_data(Address, register, value)
	return -1
'''

def writeACC(register,value):
        bus.write_byte_data(LSM303_ADDRESS_ACCEL , register, value)
        return -1

def writeMAG(register,value):
        bus.write_byte_data(LSM303_ADDRESS_MAG, register, value)
        return -1

def writeGRY(register,value):
        bus.write_byte_data(L3GD20_ADDRESS_GYRO, register, value)
        return -1

'''
def readACCAxis(axis):
        reg = LSM303_ACCEL_OUT_X_L_A
        if axis == 'x':
                acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg) 
                acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 1) 
        elif axis == 'y':
                acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 2)
                acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 3)
        else: #axis == 'z':     #implied since only 3 possible values
                acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 4)
                acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, reg + 5)
                
	acc_combined = (acc_l | acc_h <<8)
	return acc_combined  if acc_combined < 32768 else acc_combined - 65536

def readMAGAxis(axis):
        reg = LSM303_MAG_OUT_X_H_M
        if axis == 'x':
                mag_h = bus.read_byte_data(LSM303_ADDRESS_MAG, reg) 
                mag_l = bus.read_byte_data(LSM303_ADDRESS_MAG, reg + 1) 
        elif axis == 'z':
                mag_h = bus.read_byte_data(LSM303_ADDRESS_MAG, reg + 2)
                mag_l = bus.read_byte_data(LSM303_ADDRESS_MAG, reg + 3)
        else: #axis == 'y'      #implied since only 3 possible values
                mag_h = bus.read_byte_data(LSM303_ADDRESS_MAG, reg + 4)
                mag_l = bus.read_byte_data(LSM303_ADDRESS_MAG, reg + 5)
                
	mag_combined = (mag_l | mag_h <<8)
	return mag_combined  if mag_combined < 32768 else mag_combined - 65536

def readGYRAxis(axis):
        reg = L3GD20_OUT_X_L
        if axis == 'x':
                gyr_l = bus.read_byte_data(L3GD20_ADDRESS_GYRO, reg)
                gyr_h = bus.read_byte_data(L3GD20_ADDRESS_GYRO, reg + 1)
        elif axis == 'y':
                gyr_l = bus.read_byte_data(L3GD20_ADDRESS_GYRO, reg + 2)
                gyr_h = bus.read_byte_data(L3GD20_ADDRESS_GYRO, reg + 3)
        else: #axis == 'z'
                gyr_l = bus.read_byte_data(L3GD20_ADDRESS_GYRO, reg + 4)
                gyr_h = bus.read_byte_data(L3GD20_ADDRESS_GYRO, reg + 5)

        gyr_combined = (gyr_l | gyr_h <<8)
        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
'''

def readACCx():
        acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_X_L_A)
        acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_X_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCy():
        acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_Y_L_A)
        acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_Y_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCz():
        acc_l = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_Z_L_A)
        acc_h = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_Z_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readMAGx():
        mag_l = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_MAG_OUT_X_L_M)
        mag_h = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_MAG_OUT_X_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
        mag_l = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_MAG_OUT_Y_L_M)
        mag_h = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_MAG_OUT_Y_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
        mag_l = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_MAG_OUT_Z_L_M)
        mag_h = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_MAG_OUT_Z_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536



def readGYRx():
        gyr_l = bus.read_byte_data(L3GD20_ADDRESS_GYRO, L3GD20_OUT_X_L)
        gyr_h = bus.read_byte_data(L3GD20_ADDRESS_GYRO, L3GD20_OUT_X_H)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
  

def readGYRy():
        gyr_l = bus.read_byte_data(L3GD20_ADDRESS_GYRO, L3GD20_OUT_Y_L)
        gyr_h = bus.read_byte_data(L3GD20_ADDRESS_GYRO, L3GD20_OUT_Y_H)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
        gyr_l = bus.read_byte_data(L3GD20_ADDRESS_GYRO, L3GD20_OUT_Z_L)
        gyr_h = bus.read_byte_data(L3GD20_ADDRESS_GYRO, L3GD20_OUT_Z_H)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536


'''
#initialise the accelerometer
writeRegisterAxis(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_CTRL_REG1_A, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
writeRegisterAxis(LSM303_ADDRESS_ACCEL, LSM303_ACCEL_CTRL_REG2_A, 0b00100000) #+/- 16G full scale

#initialise the magnetometer
writeRegisterAxis(LSM303_ADDRESS_MAG, LSM303_CRA_REG_M, 0b11110000) #Temp enable, M data rate = 50Hz
writeRegisterAxis(LSM303_ADDRESS_MAG, LSM303_CRB_REG_M, 0b01100000) #+/-12gauss
writeRegisterAxis(LSM303_ADDRESS_MAG, LSM303_MR_REG_M, 0b00000000) #Continuous-conversion mode

#initialise the gyroscope
writeRegisterAxis(L3GD20_ADDRESS_GYRO, L3GD20_CTRL_REG1, 0b00001111) #Normal power mode, all axes enabled
writeRegisterAxis(L3GD20_ADDRESS_GYRO, L3GD20_CTRL_REG4, 0b00110000) #Continuos update, 2000 dps full scale
'''

#initialise the accelerometer
writeACC(LSM303_ACCEL_CTRL_REG1_A, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(LSM303_ACCEL_CTRL_REG2_A, 0b00100000) #+/- 16G full scale

#initialise the magnetometer
writeMAG(LSM303_CRA_REG_M, 0b11110000) #Temp enable, M data rate = 50Hz
writeMAG(LSM303_CRB_REG_M, 0b01100000) #+/-12gauss
writeMAG(LSM303_MR_REG_M, 0b00000000) #Continuous-conversion mode

#initialise the gyroscope
writeGRY(L3GD20_CTRL_REG1, 0b00001111) #Normal power mode, all axes enabled
writeGRY(L3GD20_CTRL_REG4, 0b00110000) #Continuos update, 2000 dps full scale


gyroXangle = gyroYangle = gyroZangle = 0.0
CFangleX = CFangleY = 0.0
kalmanX = kalmanY = 0.0

a = datetime.datetime.now()                                             #Gyro Timing Control


while True:
	total_heading = 0.0
	#loop = 1                     #High the loops the greater the accuracy
					#The longer the cycle
	#n = 0
	#while n < loop: #True:                    #Continous run Disabled to allow Node.js control
	#        n = n + 1

	#for num in range(0,loop):	        #Currently this loop runs for 20 reads providing greater accuracy
		
	#Read the accelerometer,gyroscope and magnetometer values
	'''
	ACCx = readACCAxis('x')
	ACCy = readACCAxis('y')
	ACCz = readACCAxis('z')
	GYRx = readGYRAxis('x')
	GYRy = readGYRAxis('y')
	GYRz = readGYRAxis('z')
	MAGx = readMAGAxis('x')
	MAGy = readMAGAxis('y')
	MAGz = readMAGAxis('z')
	'''
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()
	GYRx = readGYRx()
	GYRy = readGYRy()
	GYRz = readGYRz()
	MAGx = readMAGx()
	MAGy = readMAGy()
	MAGz = readMAGz()
	
	##Calculate loop Period(LP). How long between Gyro Reads
	b = datetime.datetime.now() - a
	a = datetime.datetime.now()
	LP = b.microseconds/(1000000*1.0)
	#print "Loop Time | %5.2f|" % ( LP ),   #Error checking stop
	
	#Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * G_GAIN
	rate_gyr_y =  GYRy * G_GAIN
	rate_gyr_z =  GYRz * G_GAIN

	#Calculate the angles from the gyro. 
	gyroXangle+=rate_gyr_x*LP
	gyroYangle+=rate_gyr_y*LP
	gyroZangle+=rate_gyr_z*LP


	##Convert Accelerometer values to degrees
	AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
	AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

	####################################################################	
	##########Direction Requirement####Correct rotation value###########
	####################################################################
	#Change the rotation value of the accelerometer to -/+ 180 and
	#move the Y axis '0' point to up.
	#
	#Two different pieces of code are used depending on how your IMU is mounted.
	#If IMU is up the correct way, IC's facing the sky, Use these lines
	AccXangle -= 180.0
	if AccYangle > 90:
		AccYangle -= 270.0
	else:
		AccYangle += 90.0
	#
	#
	#If IMU is upside down, IC's facing the Earth, using these lines
	#if AccXangle >180:
	#        AccXangle -= 360.0
	#AccYangle-=90
	#if (AccYangle >180):
	#        AccYangle -= 360.0
	############################ END ##################################


	#Complementary filter used to combine the accelerometer and gyro values.
	CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
	CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle
	
	#Kalman filter used to combine the accelerometer and gyro values.
	kalmanY = kalmanFilterY(AccYangle, rate_gyr_y,LP)
	kalmanX = kalmanFilterX(AccXangle, rate_gyr_x,LP)

	####################################################################
	##########Direction Requirement#######MAG direction ################
	####################################################################
	#If IMU is upside down, then use this line.  It isnt needed if the
	# IMU is the correct way up
	#MAGy = -MAGy
	#
	############################ END ##################################
	
	
	#Calculate heading with Radian to Degree conversion
	heading = 180 * math.atan2(MAGy,MAGx)/M_PI

	#Only have our heading between 0 and 360
	if heading < 0:
		heading += 360


	#Normalize accelerometer raw values.
	accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
	accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

	
	####################################################################
	##########Direction Requirement#####Calculate pitch and roll########
	####################################################################
	#Us these two lines when the IMU is right side up.  IC's facing sky 
	pitch = math.asin(accXnorm)
	temp = accYnorm/math.cos(pitch)
	if temp <= 1 and temp >= -1:
	    roll = -math.asin(accYnorm/math.cos(pitch))

	#
	#Us these four lines when the IMU is upside down. IC's facing earth
	#accXnorm = -accXnorm				#flip Xnorm as the IMU is upside down
	#accYnorm = -accYnorm				#flip Ynorm as the IMU is upside down
	#pitch = math.asin(accXnorm)
	#roll = math.asin(accYnorm/math.cos(pitch))
	#
	############################ END ##################################

	#Calculate the new tilt compensated values
	magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
	magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)

	#Calculate tilt compensated heading w/ Radian to Degree conversion
	tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

	if tiltCompensatedHeading < 0:
		tiltCompensatedHeading += 360


	#Error checking Section for trouble shooting
	if 0: #1:			#Change to '1' to show the angles from the accelerometer
		print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f  \033[0m  " % (AccXangle, AccYangle)),
	
	if 0: #1:			#Change to '0' to stop  showing the angles from the gyro
		print ("\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f" % (gyroXangle,gyroYangle,gyroZangle)),

	if 0: #1:			#Change to '0' to stop  showing the angles from the complementary filter
		print ("\033[1;35;40m   \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m" % (CFangleX,CFangleY)),
		
	if 0: #1:			#Change to '0' to stop  showing the heading
		print ("HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f" % (heading,tiltCompensatedHeading)),
		
	if 0: #1:			#Change to '0' to stop  showing the angles from the Kalman filter
		print ("\033[1;31;40m kalmanX %5.2f  \033[1;35;40m kalmanY %5.2f  " % (kalmanX,kalmanY))

	
	#slow program down a bit, makes the output more readable
	#time.sleep(0.5)        #disable while not using loop features
	#break                  #this is disabliling the while loop for Node.js Control
	#n = n + 1
	#Output to stdout if running stand alone or passed to node.js control program through flush call
	#print("%d,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.8f,%5.2f,%5.2f,%5.2f" % (n, AccXangle, AccYangle, gyroXangle,gyroYangle,gyroZangle,CFangleX,CFangleY, heading, tiltCompensatedHeading, kalmanX,kalmanY))
	total_heading = heading 
	#total_heading = total_heading / loop
	
	if(MAGNETIC_DECLINATION > total_heading):
		total_heading = 360 - (MAGNETIC_DECLINATION - total_heading)
	else:
		total_heading = total_heading - MAGNETIC_DECLINATION

	print("%5.8f" % (total_heading))
	sys.stdout.flush()
