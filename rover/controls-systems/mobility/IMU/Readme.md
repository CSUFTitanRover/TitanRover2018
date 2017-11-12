BNO055 9 DOF Absolute Orientation IMU

  The BNO055 IMU, developed by Adafruit, is a 3.3-5V logic board that has three 3-axis sensors.  
The Accelerometer, Gyroscope, and Magnetometer are used to measure acceleration forces, orientation 
and angular velocity, and magnetic fields respectively. The BNO reports the absolute orientation using 
two different output methods. Quaternions, a number system that extends complex numbers through a 4-D 
vector space over real numbers. Euler Angles, three angles that describe the orientation of a body with 
respect to a fixed coordinate system. Vectors are also obtained when requesting a specific data reading 
such as Magnetic Field Strength. These readings are acquired over an I2C bus.

FEATURES:
•	ARM Cortex-M0 based processor
•	Built on a fusion breakout board
  o	 Blends individual sensor data into a stable three-axis orientation
•	Three 3-axis sensors
  o	Accelerometer, Gyroscope, and Magnetometer
•	I2C native connection

DATA OUTPUT AND ACQUISITION
•	Utilizes the Adafruit_BNO055 driver library and the Adafruit_Sensor Library
•	Raw Sensor Data Functions
  o	getVector (adafruit_vector_type_t vector_type)
  o	getQuat (void)
  o	getTemp (void)

DIMENSIONS
•	Size: 20mm x 27mm x 4mm / (0.8" x 1.1" x 0.2")
•	Weight: 3g

  The BNO055 IMU does not contain any internal EEPROM. New calibrations must be performed 
on startup before absolute data can be acquired. Alternatively, manual restoration of 
previous calibration values can be performed. The calibration data will be stored until 
the BNO is powered off.
