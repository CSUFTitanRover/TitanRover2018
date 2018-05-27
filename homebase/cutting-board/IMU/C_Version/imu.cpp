#include <signal.h>
//#include <string.h>
//#include <time.h>
//#include "sensor.c"
//#include "10DOF.h"
//#include "bmp180.h"


#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <math.h>
#include <linux/i2c-dev.h>
#include "L3GD20_GYRO.h"
#include "LSM303_U.h"

#define A_GAIN 0.0573			// [deg/LSB]
#define G_GAIN 0.070			// [deg/s/LSB]
#define RAD_TO_DEG 57.29578
#define M_PI 3.14159265358979323846
#define DT 0.02				// [s/loop] loop period. 20ms
#define AA 0.97				// complementary filter constant


//int file;
void readBlock(int, uint8_t, uint8_t, uint8_t *);
void selectDevice(int, uint8_t);
void writeReg(int, uint8_t, uint8_t, uint8_t);
void readChip(int, uint8_t, uint8_t, int  *);

int main()
{
	float rate_gyr_y = 0.0;   // [deg/s]
	float rate_gyr_x = 0.0;    // [deg/s]
	float rate_gyr_z = 0.0;     // [deg/s]

	int  accRaw[3];
	int  magRaw[3];
	int  gyrRaw[3];

	float gyroXangle = 0.0;
	float gyroYangle = 0.0;
	float gyroZangle = 0.0;
	float AccYangle = 0.0;
	float AccXangle = 0.0;
	float CFangleX = 0.0;
	float CFangleY = 0.0;

	//Open the I2C Bus
	int file;
	char filename[20];
	sprintf(filename, "/dev/i2c-%d", 1);
	file = open(filename, O_RDWR);
	if (file<0) {
	        printf("Unable to open I2C bus!");
	        exit(1);
	}
	
	
	//Enable the magnetometer

	writeReg(file, LSM303_ADDRESS_MAG, LSM303_CRA_REG_M, 0b10011000);  //temp enabled at 75Hz
	writeReg(file, LSM303_ADDRESS_MAG, LSM303_CRB_REG_M, 0b11100000);  //Gain +-8.1
	writeReg(file, LSM303_ADDRESS_MAG, LSM303_MR_REG_M,  0b00000000);  //Continuous-conversion mode
	
	// Enable accelerometer.
	//writeReg(file, LSM303_ADDRESS_ACCEL, LSM303_ACCEL_CTRL_REG1_A, 0b01100111);
	writeReg(file, LSM303_ADDRESS_ACCEL, LSM303_ACCEL_CTRL_REG1_A, 0b01100111); //  z,y,x axis enabled, continuos
						  //  update, ODR 100Hz w/ cutoff 25Hz
	writeReg(file, LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_CTRL_REG2_A , 0b00100000); // +/- 16G full scale

	// Enable Gyro
	//writeReg(file, L3GD20_ADDRESS_GYRO, L3GD20_CTRL_REG1, 0b00000000);
	writeReg(file, L3GD20_ADDRESS_GYRO, L3GD20_CTRL_REG1, 0b00001111); // Normal power mode, all axes enabled	
	writeReg(file, L3GD20_ADDRESS_GYRO, L3GD20_CTRL_REG4, 0b00110000); // Continuos update, 2000 dps full scale
	
	while(1)
	{
		/*
		When rotating your magnetometer clockwise, the heading should increase. It
		should decrease when rotated counter clockwise.  If this is not the case, 
		then you need to convert the Y axis. This will happen if the magnetometer is
		upside down.
		*/
		readChip(file, LSM303_ADDRESS_MAG, LSM303_MAG_OUT_X_H_M, magRaw);
		readChip(file, LSM303_ADDRESS_ACCEL, LSM303_ACCEL_OUT_X_L_A, accRaw);
		readChip(file, L3GD20_ADDRESS_GYRO, L3GD20_OUT_X_L, gyrRaw);
	        

		float heading = 180 * atan2(magRaw[1],magRaw[0])/M_PI;
	 	
		//Convert heading to 0 - 360
	        if(heading < 0)
	              heading += 360;
	 
       		printf("heading %7.3f \t ", heading);
	        
		printf("magRaw X %i    \tmagRaw Y %i \tMagRaw Z %i \n\n", magRaw[0],
								magRaw[1],magRaw[2]);
	
	
		//Convert Gyro raw to degrees per second
		rate_gyr_x = (float) gyrRaw[0]  * G_GAIN;
		rate_gyr_y = (float) gyrRaw[1]  * G_GAIN;
		rate_gyr_z = (float) gyrRaw[2]  * G_GAIN;

		//Calculate the angles from the gyro
		gyroXangle+=rate_gyr_x*DT;
		gyroYangle+=rate_gyr_y*DT;
		gyroZangle+=rate_gyr_z*DT;

		//Convert Accelerometer values to degrees
 		AccXangle = (float) (atan2(accRaw[1],accRaw[2])+M_PI)*RAD_TO_DEG;
		AccYangle = (float) (atan2(accRaw[2],accRaw[0])+M_PI)*RAD_TO_DEG;

		AccXangle -= (float)180.0;
		if (AccYangle > 90)
      			AccYangle -= (float)270;
		else
       			AccYangle += (float)90;

		//Combining Angles from the Accelerometer and Gyro
		CFangleX=AA*(CFangleX+rate_gyr_x*DT) +(1 - AA) * AccXangle;
		CFangleY=AA*(CFangleY+rate_gyr_y*DT) +(1 - AA) * AccYangle;

		printf ("   GyroX  %7.3f \t AccXangle \e[m %7.3f \t \033[22;31mCFangleX %7.3f\033[0m\t GyroY  %7.3f \t AccYangle %7.3f \t \033[22;36mCFangleY %7.3f\t\033[0m\n",gyroXangle,AccXangle,CFangleX,gyroYangle,AccYangle,CFangleY);

		usleep(250000);
	
	}

}


void  readBlock(int file, uint8_t command, uint8_t size, uint8_t *data)
{
    int result = i2c_smbus_read_i2c_block_data(file, command, size, data);
    if (result != size)
    {
       printf("Failed to read block from I2C.");
        exit(1);
    }
}

void selectDevice(int file, uint8_t addr)
{
	char device[3];
	
	if (ioctl(file, I2C_SLAVE, addr) < 0) {
		printf("Failed to select I2C device at %s", device);
	}
}

//The i2c_smbus_write_byte_data() function can be used to write 
//	to a device’s register on the i2c bus.
//i2c_smbus_write_byte_data (struct i2c_client * client, u8 command, u8 value);

void writeReg(int file, uint8_t chipReg, uint8_t reg, uint8_t value)
{
    selectDevice(file, chipReg);
    int result = i2c_smbus_write_byte_data(file, reg, value);
    if (result == -1)
    {
        printf("Failed to write byte to I2C Gyr.");
        exit(1);
    }
}

void readChip(int file, uint8_t chipAddress, uint8_t regStartAddress, int  *m)
{
        uint8_t block[6];
	selectDevice(file,chipAddress);
 
        readBlock(file, 0x80 | regStartAddress, sizeof(block), block);
        *m = (int16_t)(block[0] | block[1] << 8);
        *(m+1) = (int16_t)(block[2] | block[3] << 8);
        *(m+2) = (int16_t)(block[4] | block[5] << 8);
}
