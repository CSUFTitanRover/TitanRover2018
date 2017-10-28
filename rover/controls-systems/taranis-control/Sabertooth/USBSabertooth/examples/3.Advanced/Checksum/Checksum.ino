// Checksum Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

// This sample changes the type of error detection that is done.
// It uses checksums to achieve a faster update rate than the Sweep sample.
//
// The tradeoffs are as follows:
//                                     |  Checksum  |    CRC    |
// |-----------------------------------|------------|-----------|
// | Command Size                      |   8 bytes  | 10 bytes  |
// | Max Command Rate at 9600 Baud     | 120 cmd/s  | 96 cmd/s  |
// | Detectable Bit Flips (Worst-Case) |   1 (HD=2) |  5 (HD=6) |
// |-----------------------------------|------------|-----------|
//
// If you want to, you can require the use of CRC-protected commands
// with DEScribe. Go to DEScribe's Serial tab to find this option.
//
// This tab also lets you change the serial baud rate. Increasing the
// baud rate is, in most situations, a better way to increase the max
// command rate than weakening error detection.

USBSabertoothSerial C;
USBSabertooth       ST(C, 128);
                                        
void setup()
{
  SabertoothTXPinSerial.begin(9600);
  
  ST.useChecksum(); // ST.useCRC(); is the default.
}

void loop()
{
  int power;
  
  // Ramp motor 1 from -2047 to 2047 (full reverse to full forward),
  // waiting 9 ms (1/111th of a second) per step.
  for (power = -2047; power <= 2047; power += 8)
  {
    ST.motor(1, power);
    delay(9);
  }
  
  // Now go back the way we came.
  for (power = 2047; power >= -2047; power -= 8)
  {
    ST.motor(1, power);
    delay(9);
  }
}

