/*
	K_Series.h -Library for interfacing with a K-series sensor
	Created by Jason Berger
	for CO2METER.com
	OCT-12-2012

*/


#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

#ifndef kSeries_h
#define kSeries_h

#include <SoftwareSerial.h> 	//Virtual Serial library

class kSeries
{
  public:
    kSeries(uint8_t Rx, uint8_t Tx);
    double getCO2(char format);
	double getTemp(char unit);
	double getRH();
	bool _K33;
	bool _ASCII;
	int cmdInit();
  private:
	SoftwareSerial* _Serial;
	void chkSensorType();
	void chkASCII();
	void chkK33();
	int sendRequest(int reqType, int respSize, int respInd);
	long getResp(int size, int strt);	
	void wait(int ms);
};

#endif