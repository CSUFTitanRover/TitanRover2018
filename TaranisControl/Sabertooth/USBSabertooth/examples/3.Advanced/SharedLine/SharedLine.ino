// Shared Line Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

// Up to 8 Sabertooth/SyRen motor drivers can share the same S1 line.
// This sample uses three: address 128 and 129 on ST1[0] and ST1[2],
// and address 130 on ST2.
//
// To change the address of a USB Sabertooth motor driver, go to the
// Serial tab in DEScribe. DEScribe can be downloaded from
//   http://www.dimensionengineering.com/describe
USBSabertoothSerial C;
USBSabertooth       ST1[2] = { USBSabertooth(C, 128), USBSabertooth(C, 129) };
USBSabertooth       ST2(C, 130);

void setup()
{
  SabertoothTXPinSerial.begin(9600);
}

void loop()
{
  // ST1[0] (address 128) has power  800 (of 2047 max) on M1,
  // ST1[1] (address 129) has power 1000 (of 2047 max) on M2, and
  // ST2    (address 130) we'll do tank-style and have it drive 300 and turn right 800.
  // Do this for 5 seconds.
  ST1[0].motor(1, 800);
  ST1[1].motor(2, 1000);
  ST2.drive(300);
  ST2.turn(800);
  delay(5000);
  
  // And now let's stop for 5 seconds, except address 130 -- we'll let it stop and turn left...
  ST1[0].motor(1, 0);
  ST1[1].motor(2, 0);
  ST2.drive(0);
  ST2.turn(-600);  
  delay(5000);
}

