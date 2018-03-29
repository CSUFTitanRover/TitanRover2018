/*
	K_Series.cpp -Library for interfacing with a K-series sensor
	Created by Jason Berger
	for CO2METER.com
	OCT-12-2012

*/

//#include "Arduino.h"
#include "kSeries.h"
#include "SoftwareSerial.h" 	//Virtual Serial library

//SoftwareSerial* _Serial;

//commands

byte cmd_read_CO2[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25};	//type [0]
byte cmd_read_Temp[] = {0xFE, 0X44, 0X00, 0X12, 0X02, 0X94, 0X45};	//type [1]
byte cmd_read_RH[] = {0xFE, 0x44, 0x00, 0x14, 0x02, 0x97, 0xE5 };	//type [2]
byte cmd_init[] = {0xFE, 0X41, 0X00, 0X60, 0X01, 0X35, 0XE8, 0x53}; //type [3]

kSeries :: kSeries(uint8_t Rx,uint8_t Tx)
{
	this->_Serial = new SoftwareSerial(Rx,Tx);
	this->_Serial->begin(9600);
	//chkSensorType();
}

int kSeries :: cmdInit()
{
	return sendRequest(3,4,0);
}
double kSeries :: getCO2(char format)
{
	double co2 = sendRequest(0,7,3);
	if(format == '%')
		co2 /= 10000;
		
	return co2;
}
double kSeries :: getTemp(char unit)
{
	double temp = sendRequest(1,7,3);
	temp/=100;
	if ((unit =='f') || (unit == 'F'))
		temp = (temp * 9 / 5) + 32;
	
	return temp;
}
double kSeries :: getRH()
{
	double RH = sendRequest(2,7,3);
	RH/=100;
	return RH;
}
void kSeries :: chkSensorType()
{
	chkASCII();
	chkK33();
}

void kSeries::chkK33()
{
	int temp = sendRequest(1,7,3);
	if(temp > -255)
		_K33 = true;
	else
		_K33 = false;
	
}

void kSeries :: chkASCII()
{
	int timeout=0;
	while(this->_Serial->available() == 0)
	{
		if(timeout > 100)
		{
			_ASCII =false;
			break;
		}
		timeout++;
		delay(25);
	}	
	if (timeout < 200)
		_ASCII = true;
	
}

int kSeries :: sendRequest(int reqType, int respSize, int respInd)
{
	long Val=-255;
	int cmdTimeout =0;
	while(this->_Serial->available() == 0)	//send read command in a loop until we see a response
    { 
		switch(reqType)
		{
			case 0:
				this->_Serial->write(cmd_read_CO2,7);
				break;
			case 1:
				this->_Serial->write(cmd_read_Temp,7);
				break;
			case 2:
				this->_Serial->write(cmd_read_RH,7);
				break;
			case 3:
				this->_Serial->write(cmd_init,8);
				break;
			default:
				return -256;
				break;
		}
		cmdTimeout++;
		if(cmdTimeout > 20)
			return -203;
      wait(130);					//give some time after each request for a response
    }
	
	int timeOut=0;	//initialize a timeout counter
	
	while(this->_Serial->available() < 7)	//loop through until we have are 7-byte response
	{ 
		if(timeOut > 40);			//after 40 loops, break out and try again
			break;
		timeOut++;
		delay(5);
	}
	
	if(this->_Serial->available() == 7)		//if we have our 7-byte response get value
			 Val = getResp(respSize,respInd);
	else							//if we dont i.e. our request timed out
	{
		Val = -300;
		while(this->_Serial->available() > 0)	//loop through and flush any bytes we did receiver so they dont throw the next packet off track
		{
				Val++;
				this->_Serial->read();
		}	
	}
	return Val;
}

long kSeries :: getResp(int size, int strt)
{
	byte packet[size];
    for(int i=0; i<size; i++)
    {
		packet[i] = this->_Serial->read();                   //create array from packet
    }
	
    int high = packet[strt];                        //high byte for value is 4th byte in packet in the packet
    int low = packet[strt+1];                         //low byte for value is 5th byte in the packet

  
    unsigned long val = high*256 + low;                //combine high byte and low byte
    return val;
}

void kSeries :: wait(int ms)
{
	long start = millis();
	long tmp = millis();
	while ((tmp - start) < ms)
	{
		tmp=millis();
	}
}