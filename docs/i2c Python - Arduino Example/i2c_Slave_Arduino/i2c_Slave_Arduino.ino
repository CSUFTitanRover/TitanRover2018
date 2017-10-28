#include <Wire.h>
int x = 0;
int y = 0;
bool runTotal = false;

void setup()
{
  Wire.begin(0x4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  
}

void loop()
{
  if(runTotal)
  {
    Serial.print(x);
    Serial.print(' ');
    Serial.println(y);
    runTotal = false;
  } 
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  //Serial.println(x);
  while(0 < Wire.available()) // loop through all
  {
    x = Wire.read();    // receive byte as an integer
    y = Wire.read();    // receive byte as an integer
  }
  if(x ==  253)
    runTotal = true;
}
