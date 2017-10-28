#include <Wire.h>
#include "Sabertooth.h"
#include <SoftwareSerial.h>
#define SLAVE_ADDRESS 0x04
//#include "SabertoothSimplified.h"

SoftwareSerial SWSerial(NOT_A_PIN,11);
Sabertooth ST(128,SWSerial);

int number = 0;
boolean runMotor = false;

void setup()
{
  SWSerial.begin(9600);
  //Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

  void loop()
{
  if(runMotor) {
    int power = -127;
    for(power = -127; power <=127; power++)
    {
      ST.motor(1,power);
      //Serial.println(power);
      delay(20);
    }
    
    for(power = 127; power >= -127; power--)
    {
      ST.motor(1,power);
      //Serial.println(power);
      delay(20);
    }
    ST.motor(1,0);
    runMotor = false;
  }
}

void receiveData(int byteCount){
  while(Wire.available()) {
    number = Wire.read();
    if (number == 1){
      runMotor = true; 
    }
  }
}

void sendData() {
  Wire.write(number);
}
