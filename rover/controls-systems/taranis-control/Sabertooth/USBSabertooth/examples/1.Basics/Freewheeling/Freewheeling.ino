// Freewheeling Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

// Instead of braking, this sample lets the motor freewheel.

USBSabertoothSerial C; // Use the Arduino TX pin. It connects to S1.
                       // See the SoftwareSerial example in 3.Advanced for how to use other pins.

USBSabertooth ST(C, 128); // The USB Sabertooth is on address 128 (unless you've changed it with DEScribe).
                          // We'll name its object ST.
                          //
                          // If you've set up your Sabertooth on a different address, of course change
                          // that here. For how to configure the Sabertooth, see the DIP Switch Wizard at
                          //   http://www.dimensionengineering.com/datasheets/USBSabertoothDIPWizard/start.htm
                          // Be sure to select Packet Serial Mode for use with this library.
                                        
void setup()
{
  SabertoothTXPinSerial.begin(9600); // 9600 is the default baud rate for Sabertooth Packet Serial.
                                     // You can change this with the DEScribe software, available at
                                     //   http://www.dimensionengineering.com/describe
}

void loop()
{
  ST.freewheel(1, false); // Turn off freewheeling.
  ST.motor(1, 2047);      // Go forward at full power.
  delay(1000);            // Wait 1 second.
  ST.freewheel(1, true);  // Turn on freewheeling.
  delay(2000);            // Wait 2 seconds.
  ST.motor(1, -2047);     // Reverse at full power.
  ST.freewheel(1, false); // Turn off freewheeling.
  delay(1000);            // Wait 1 seconds.
  ST.freewheel(1, true);  // Turn on freewheeling.
  delay(2000);
}

