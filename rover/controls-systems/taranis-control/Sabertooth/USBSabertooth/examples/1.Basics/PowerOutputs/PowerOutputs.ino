// Power Outputs Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

// This example treats the power outputs P1 and P2 as controllable outputs,
// useful for fans, lights, single-direction motors, etc.
//
// The power outputs are not, by default, controllable outputs.
// You will need to use the DEScribe software, available at
//   http://www.dimensionengineering.com/describe
// To configure them, in DEScribe,
//   (1) Connect and Download Settings,
//   (2) On the Power Outputs tab, set Mode to 'Controllable Output', and then
//   (3) Upload Settings to Device
// This sample will then work.

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
  SabertoothTXPinSerial.begin(9600);
}

void loop()
{
  int value;
  
  // Ramp power output 1 from -2047 to 2047 (off to full power),
  // waiting 20 ms (1/50th of a second) per step.
  for (value = -2047; value <= 2047; value += 16)
  {
    ST.power(1, value);
    delay(20);
  }
  
  // Now go back the way we came.
  for (value = 2047; value >= -2047; value -= 16)
  {
    ST.power(1, value); // Tip: Typing ST.power(value) does the same thing as ST.power(1, value).
    delay(20);          //      If you often use only one power output, this alternative can save you typing.
  }
}

