// Set Serial Timeout Sample for USB Sabertooth Packet Serial
// Copyright (c) 2012-2013 Dimension Engineering LLC
// See license.txt for license details.

#include <USBSabertooth.h>

USBSabertoothSerial C;
USBSabertooth       ST(C, 128);

void setup()
{
  SabertoothTXPinSerial.begin(9600);
  
  // Set a timeout of 1500 ms here.
  // A value of 0 resets the serial timeout to its default (normally, disabled).
  // You can also set the serial timeout in DEScribe, available at
  //   http://www.dimensionengineering.com/describe
  ST.setTimeout(1500);
}

void loop()
{
  // Set motor 1 to reverse 400 (out of 2047), and sleep for 5 seconds.
  // Notice how it cuts out after 1.5 seconds -- this is the serial timeout in action.
  // Since we configured it in setup() for 1.5 second, 1.5 second without any new
  // commands will cause the motors to stop.
  ST.motor(1, -400);
  delay(5000);
  
  // Why do this?
  // If your program crashes, or the signal wire is not working properly,
  // the Sabertooth will stop receiving commands from the Arduino.
  // With a timeout, your robot will stop.
  //
  // So, serial timeout is primarily a safety feature. That being the case,
  // it's best to set the serial timeout in DEScribe if you can -- if the
  // signal line is noisy when the command is sent, it may be lost. DEScribe
  // settings are saved on the motor driver, eliminating that possibility.
}

