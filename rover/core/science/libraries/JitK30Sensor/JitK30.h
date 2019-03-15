/*
 * Written by Jithin Eapen- on 29th March 2018
 * I2C code for K-30 CO2 sensor
*/

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

int readCO2();
