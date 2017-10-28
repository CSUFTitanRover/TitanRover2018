// Software Serial Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <SoftwareSerial.h>
#include <USBSabertooth.h>

SoftwareSerial      SWSerial(NOT_A_PIN, 11); // RX on no pin (unused), TX on pin 11 (to S1).
USBSabertoothSerial C(SWSerial);             // Use SWSerial as the serial port.
USBSabertooth       ST(C, 128);              // Use address 128.

void setup()
{
  SWSerial.begin(9600);
}

void loop()
{
  int power;
  
  // Ramp motor 1 from -2047 to 2047 (full reverse to full forward),
  // waiting 20 ms (1/50th of a second) per step.
  for (power = -2047; power <= 2047; power += 16)
  {
    ST.motor(1, power);
    delay(20);
  }
  
  // Now go back the way we came.
  for (power = 2047; power >= -2047; power -= 16)
  {
    ST.motor(1, power);
    delay(20);
  }
}

