// Tank-Style (Diff-Drive) Sweep Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

USBSabertoothSerial C; // Use the Arduino TX pin. It connects to S1.
                       // See the SoftwareSerial example in 3.Advanced for how to use other pins.

USBSabertooth ST(C, 128); // The USB Sabertooth is on address 128 (unless you've changed it with DEScribe).
                          // We'll name its object ST.
                          //
                          // If you've set up your Sabertooth on a different address, of course change
                          // that here. For how to configure the Sabertooth, see the DIP Switch Wizard at
                          //   http://www.dimensionengineering.com/datasheets/USBSabertoothDIPWizard/start.htm
                          // Be sure to select Packet Serial Mode for use with this library.
                          //
                          // The USBSabertooth library exposes features that only exist on USB-enabled Sabertooth motor drivers, such as
                          // 12-bit motor outputs, power outputs, control over freewheeling, motor current read-back, and User Mode variables.
                          // If you do not need these features, and want your code to be compatible with all Sabertooth/SyRen motor drivers,
                          // including those that are not USB-enabled, use the Sabertooth library instead.
                                        
void setup()
{
  SabertoothTXPinSerial.begin(9600); // 9600 is the default baud rate for Sabertooth Packet Serial.
                                     // You can change this with the DEScribe software, available at
                                     //   http://www.dimensionengineering.com/describe
             
  ST.drive(0); // The Sabertooth won't act on mixed mode packet serial commands until
  ST.turn(0);  // it has received power levels for BOTH throttle and turning, since it
               // mixes the two together to get diff-drive power levels for both motors.
}

// The SLOW ramp here is turning, and the FAST ramp is throttle.
// If that's the opposite of what you're seeing, swap M2A and M2B.
void loop()
{
  int power;
  
  // Don't turn. Ramp from going backwards to going forwards, waiting 20 ms (1/50th of a second) per step of 16.
  for (power = -2047; power <= 2047; power += 16)
  {
    ST.drive(power);
    delay(20);
  }
  
  // Now, let's use a power level of 400 (out of 2047) forward.
  // This way, our turning will have a radius.
  ST.drive(400);
  
  // Ramp turning from full left to full right SLOWLY by waiting 20 ms (1/50th of a second) per step of 4.
  for (power = -2047; power <= 2047; power += 4)
  {
    ST.turn(power);
    delay(20);
  }
  
  // Now stop turning, and stop driving.
  ST.turn(0);
  ST.drive(0);
  
  // Wait a bit. This is so you can catch your robot if you want to. :-)
  delay(5000);
}

