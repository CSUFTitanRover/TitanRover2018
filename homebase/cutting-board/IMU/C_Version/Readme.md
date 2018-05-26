File imu.cpp
==============================================================================================================================

This program will read the IMU registers and provide heading, pitch, roll angles.  Written to function with the Adafruit 10-DOF 
IMU Breakout board which has the following chips:

1. LSM303DLHC - Accelerometer Compass
2. L3DG20H - Gyroscope
3. BMP180 - Barometric/Temperature sensor

This code will pull all values from the IMU and place them in a outfile to be
read by the Node.js Rover systems.

Communication: I2C

==============================================================================================================================

Version:  1.0 
=============
Date:  11/12/16

Provides output for all axis information.  Software bug allowing the axis readings to flip from positive to negative.


Version:   1.1
=============
Date:  11/16/16

- Improved code standards combining commonly used function call to each chip seperately into one call.  Added chip address to function paramaters and removed access functions.


Version:   1.2
=============
Date:  11/25/16

- Reduced extra code in .h to only required constant addresses needed for project all other code commented out.
- Moved required addresses to top of file


Version:   1.4
=============
Date:  12/02/16

- Found system bug in orginal code with wrong address in function paramater causing stability issues.


Version:  Cancelled code sequence
=============
Date:  12/15/16

- After researching the outfile functions in comparison to the direct script 
communication between Python and Node.js I decided to rewrite the IMU process in 
Python Script.
