#include <Wire.h>
#include <Servo.h>
#define SLAVE_ADDRESS 0x04

Servo myservo;
int number = 0;
int state = 0;
int pos = 0;
boolean moveServo = false;

void setup() {
  
  pinMode(13, OUTPUT);
  myservo.attach(9);
  
  Serial.begin(9600);
  
  // Initialize I2C as slave
  Wire.begin(SLAVE_ADDRESS);  
  // Define callbacks for I2C communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

// Callback for received data
void receiveData(int byteCount)
{
  // While the I2C connection is open
  while(Wire.available()) 
  {
    number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);
    
    // If input from python code is 1 (led) calls toggleLed function
    if (number == 1)
    {
      toggleLed();
    }
    // If input from python code is 2 (servo) calls sweepServo function
    else if(number == 2) 
    {
      sweepServo();  
    } 
  }
}

// Callback for sending data
void sendData()
{
Wire.write(number);
// Resets python input
number = 0;
}

// Toggles LED on and off
void toggleLed() 
{
  if (state == 0)
  {
    digitalWrite(13, HIGH); // Set the LED on
    state = 1;
  }
  else
  {
    digitalWrite(13, LOW); // Set the LED off
    state = 0;
  }
}

// 180 degree servo sweep
void sweepServo()
{
  for(pos = 0; pos < 180; pos += 1)
  {                                   
    myservo.write(pos);              
    delay(15);                        
  } 
  for(pos = 180; pos>=1; pos-=1)      
  {                                
    myservo.write(pos);               
    delay(15);
  }
  moveServo = 0;
}
