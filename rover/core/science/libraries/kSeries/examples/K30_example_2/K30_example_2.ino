/*
 Reports values from a K-series sensor back to the computer
 written by Jason Berger
 Co2Meter.com
*/
#include "kSeries.h" //include kSeries Library
kSeries K_30(12,13); //Initialize a kSeries Sensor with pin 12 as Rx and 13 as Tx
void setup()
{
 Serial.begin(9600); //start a serial port to communicate with the computer
 Serial.println("   AN-216  Example 2:  uses the kSeries.h library");
}
void loop()
{
 double co2 = K_30.getCO2('p'); //returns co2 value in ppm ('p') or percent ('%')

 Serial.print("Co2 ppm = ");
 Serial.println(co2); //print value
 delay(1500); //wait 1.5 seconds
}
