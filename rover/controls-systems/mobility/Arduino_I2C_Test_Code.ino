#include <Wire.h>
#include <Servo.h>
#include <string.h>
#define SLAVE_ADDRESS 0x04

Servo myservo;

int number = 0;
String str;
int state = 0;
int pos = 0;
boolean moveServo = false;

void setup() {
  pinMode(13, OUTPUT);
  myservo.attach(9);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void loop() {
  delay(100);
  // The servo sweep has to be in the loop() area for it to function correctly. I added a run condition for the servor sweep that is toggled by the Python Script
  // From my understanding the receive data event is inside interrupt serving which doesn't allow further interrupts to take place until you're out of the receiveData function.
  if (moveServo) {
        for(pos = 0; pos < 180; pos += 1)   //Basic 180 degree servo sweep 
      {                                   
        myservo.write(pos);              
        delay(15);                        
      } 
      for(pos = 180; pos>=1; pos-=1)      
      {                                
        myservo.write(pos);               
        delay(15);                       // End sweep
      }
      moveServo = 0;
  } 
}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
    number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);
    //Serial.println(str);
    
    // If input from python script input is 1.
    if (number == 1){
      if (state == 0){
        digitalWrite(13, HIGH); // set the LED on
        state = 1;
      }
      else{
        digitalWrite(13, LOW); // set the LED off
        state = 0;
      }
    }
    // If input from the python script input is 2.
    else if(number == 2) {
      // Changes start condition for the for loop of moving the servo
      moveServo = true;  
    } 
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}


