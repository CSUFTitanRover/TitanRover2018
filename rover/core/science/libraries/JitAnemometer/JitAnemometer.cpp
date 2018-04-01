/*
 * Written by Jithin Eapen- on 29th March 2018
 * code for reading wind speed from anemometer
*/


#include <Wire.h>

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#define PinAnenometer A2




float readWindSpeed()
{
	
	float voltageConversionConstant = .004882814;
	int sensorValue = 0;
	float sensorVoltage = 0;

	float windSpeed = 0; // Wind speed in meters per second (m/s)


	float voltageMin = 0.4; // Mininum output voltage from anemometer in mV.
	float windSpeedMin = 0; // Wind speed in meters/sec corresponding to minimum voltage

	float voltageMax = 2.0; // Maximum output voltage from anemometer in mV.
	float windSpeedMax = 32; // Wind speed in meters/sec corresponding to maximum voltage


	// put your main code here, to run repeatedly:
	sensorValue = analogRead(PinAnenometer); //Get a value between 0 and 1023 from the analog pin connected to the anemometer
	sensorVoltage = sensorValue * voltageConversionConstant; //Convert sensor value to actual voltage
	

	if(sensorVoltage <= voltageMin) 
	{ 
	windSpeed = 0; //Check if voltage is below minimum value. If so, set wind speed to zero. 
	} 
	else 
	{ 
	windSpeed = ((sensorVoltage - voltageMin) * windSpeedMax / (voltageMax - voltageMin)); // * 2.23694);    //For voltages above minimum value, use the linear relationship to calculate wind speed. 
	}
 


	return(windSpeed);
};
