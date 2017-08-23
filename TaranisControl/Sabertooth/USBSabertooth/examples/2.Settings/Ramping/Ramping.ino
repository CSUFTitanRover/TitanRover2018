// Set Ramping Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

USBSabertoothSerial C;
USBSabertooth       ST(C, 128);

void setup()
{
  SabertoothTXPinSerial.begin(9600);
  
  // Ramping values run from -16383 (fast) to 2047 (slow).
  // -16383 is equivalent to turning off ramping.
  ST.setRamping(1980); // (approximately 2 seconds)
}

void loop()
{
  // Full forward, both motors.
  ST.motor(1, 2047);
  ST.motor(2, 2047);
  delay(5000);
  
  // Full reverse
  ST.motor(1, -2047);
  ST.motor(2, -2047);
  delay(5000);
}

