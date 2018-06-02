
############################################################################
# Copyright (C) 2008 - 2015 Bosch Sensortec GmbH
#
# File : bmp180.h
#
# Date : 20150327
#
# Revision : 2.2.2
#
# Usage: Sensor Driver for BMP180 sensor
#
############################################################################

#file bmp180.py
#	brief Header file for all define constants and function prototypes


############################################################################
##	I2C ADDRESS DEFINITION OF BMP180       
############################################################################
#BMP180 I2C Address#
BMP180_ADDR                                 =   0x77


############################################################################
##		ERROR CODE DEFINITIONS    
############################################################################
#E_BMP_NULL_PTR                                 =   ((s8)-127)
#E_BMP_COMM_RES                                 =   ((s8)-1)
#E_BMP_OUT_OF_RANGE                             =   ((s8)-2)


############################################################################
##			CONSTANTS       
############################################################################
#BMP180_RETURN_FUNCTION_TYPE			s8
#BMP180_INIT_VALUE				((u8)0)
#BMP180_INITIALIZE_OVERSAMP_SETTING_U8X		((u8)0)
#BMP180_INITIALIZE_SW_OVERSAMP_U8X		((u8)0)
#BMP180_INITIALIZE_NUMBER_OF_SAMPLES_U8X	((u8)1)
#BMP180_GEN_READ_WRITE_DATA_LENGTH		((u8)1)
#BMP180_TEMPERATURE_DATA_LENGTH			((u8)2)
#BMP180_PRESSURE_DATA_LENGTH			((u8)3)
#BMP180_SW_OVERSAMP_U8X				((u8)1)
#BMP180_OVERSAMP_SETTING_U8X			((u8)3)
#BMP180_2MS_DELAY_U8X				(2)
#BMP180_3MS_DELAY_U8X				(3)
#BMP180_AVERAGE_U8X				(3)
#BMP180_INVALID_DATA				(0)
#BMP180_CHECK_DIVISOR				(0)
#BMP180_DATA_MEASURE				(3)
#BMP180_CALCULATE_TRUE_PRESSURE			(8)
#BMP180_CALCULATE_TRUE_TEMPERATURE		(8)
#BMP180_SHIFT_BIT_POSITION_BY_01_BIT		(1)
#BMP180_SHIFT_BIT_POSITION_BY_02_BITS		(2)
#BMP180_SHIFT_BIT_POSITION_BY_04_BITS		(4)
#BMP180_SHIFT_BIT_POSITION_BY_06_BITS		(6)
#BMP180_SHIFT_BIT_POSITION_BY_08_BITS		(8)
#BMP180_SHIFT_BIT_POSITION_BY_11_BITS		(11)
#BMP180_SHIFT_BIT_POSITION_BY_12_BITS		(12)
#BMP180_SHIFT_BIT_POSITION_BY_13_BITS		(13)
#BMP180_SHIFT_BIT_POSITION_BY_15_BITS		(15)
#BMP180_SHIFT_BIT_POSITION_BY_16_BITS		(16)


############################################################################
##			REGISTER ADDRESS DEFINITION
############################################################################
#register definitions #

BMP180_START                                 =   (0xAA)
BMP180_PROM_DATA__LEN                        =   (22)

BMP180_CHIP_ID_REG                           =   (0xD0)
BMP180_VERSION_REG                           =   (0xD1)

BMP180_CTRL_MEAS_REG                         =   (0xF4)
BMP180_ADC_OUT_MSB_REG                       =   (0xF6)
BMP180_ADC_OUT_LSB_REG                       =   (0xF7)

BMP180_SOFT_RESET_REG                        =   (0xE0)

BMP180_T_MEASURE                             =   (0x2E)	# temperature measurement #
BMP180_P_MEASURE                             =   (0x34)	# pressure measurement#
BMP180_TEMP_CONVERSION_TIME                  =   (5)	# TO be spec'd by GL or SB#

BMP180_PARAM_MG                              =   (3038)
BMP180_PARAM_MH                              =   (-7357)
BMP180_PARAM_MI                              =   (3791)


############################################################################
##			ARRAY SIZE DEFINITIONS
############################################################################
#BMP180_TEMPERATURE_DATA_BYTES		(2)
#BMP180_PRESSURE_DATA_BYTES		(3)
#BMP180_TEMPERATURE_LSB_DATA		(1)
#BMP180_TEMPERATURE_MSB_DATA		(0)
#BMP180_PRESSURE_MSB_DATA		(0)
#BMP180_PRESSURE_LSB_DATA		(1)
#BMP180_PRESSURE_XLSB_DATA		(2)

#BMP180_CALIB_DATA_SIZE			(22)
#BMP180_CALIB_PARAM_AC1_MSB		(0)
#BMP180_CALIB_PARAM_AC1_LSB		(1)
#BMP180_CALIB_PARAM_AC2_MSB		(2)
#BMP180_CALIB_PARAM_AC2_LSB		(3)
#BMP180_CALIB_PARAM_AC3_MSB		(4)
#BMP180_CALIB_PARAM_AC3_LSB		(5)
#BMP180_CALIB_PARAM_AC4_MSB		(6)
#BMP180_CALIB_PARAM_AC4_LSB		(7)
#BMP180_CALIB_PARAM_AC5_MSB		(8)
#BMP180_CALIB_PARAM_AC5_LSB		(9)
#BMP180_CALIB_PARAM_AC6_MSB		(10)
#BMP180_CALIB_PARAM_AC6_LSB		(11)
#BMP180_CALIB_PARAM_B1_MSB		(12)
#BMP180_CALIB_PARAM_B1_LSB		(13)
#BMP180_CALIB_PARAM_B2_MSB		(14)
#BMP180_CALIB_PARAM_B2_LSB		(15)
#BMP180_CALIB_PARAM_MB_MSB		(16)
#BMP180_CALIB_PARAM_MB_LSB		(17)
#BMP180_CALIB_PARAM_MC_MSB		(18)
#BMP180_CALIB_PARAM_MC_LSB		(19)
#BMP180_CALIB_PARAM_MD_MSB		(20)
#BMP180_CALIB_PARAM_MD_LSB		(21)

############################################################################
##		BIT MASK, LENGTH AND POSITION FOR REGISTERS
############################################################################


############################################################################
##	BIT MASK, LENGTH AND POSITION FOR CHIP ID REGISTERS
############################################################################
BMP180_CHIP_ID__POS                                    =   (0)
BMP180_CHIP_ID__MSK                                    =   (0xFF)
BMP180_CHIP_ID__LEN                                    =   (8)
BMP180_CHIP_ID__REG                                    =   (BMP180_CHIP_ID_REG)


############################################################################
##	BIT MASK, LENGTH AND POSITION FOR ML VERSION
############################################################################
BMP180_ML_VERSION__POS                                 =   (0)
BMP180_ML_VERSION__LEN                                 =   (4)
BMP180_ML_VERSION__MSK                                 =   (0x0F)
BMP180_ML_VERSION__REG                                 =   (BMP180_VERSION_REG)


############################################################################
##name	BIT MASK, LENGTH AND POSITION FOR AL VERSION
############################################################################
BMP180_AL_VERSION__POS                                 =   (4)
BMP180_AL_VERSION__LEN                                 =   (4)
BMP180_AL_VERSION__MSK                                 =   (0xF0)
BMP180_AL_VERSION__REG                                 =   (BMP180_VERSION_REG)


############################################################################
##			FUNCTION FOR CALIBRATION 
############################################################################
#
#	@brief this function used for read the calibration
#	parameter from the register
#
#	Parameter   |  MSB    |  LSB    |  bit
#	------------|---------|---------|-----------
#	     AC1    |  0xAA   | 0xAB    | 0 to 7
#	     AC2    |  0xAC   | 0xAD    | 0 to 7
#	     AC3    |  0xAE   | 0xAF    | 0 to 7
#	     AC4    |  0xB0   | 0xB1    | 0 to 7
#	     AC5    |  0xB2   | 0xB3    | 0 to 7
#	     AC6    |  0xB4   | 0xB5    | 0 to 7
#	     B1     |  0xB6   | 0xB7    | 0 to 7
#	     B2     |  0xB8   | 0xB9    | 0 to 7
#	     MB     |  0xBA   | 0xBB    | 0 to 7
#	     MC     |  0xBC   | 0xBD    | 0 to 7
#	     MD     |  0xBE   | 0xBF    | 0 to 7
#
#
#	@return results of bus communication function
#	@retval 0 -> Success
#	@retval -1 -> Error
#
