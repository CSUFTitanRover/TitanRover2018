// Timothy Parks - Titan Rover Controls Lead

//

// This sketch will operate the individual Arduino Mini Pro for a specific joint. The

//  code reads if the Mega is enabling the joint or if the Kinematics software is sending 

//  a step movement count.

bool debug = true;                     // Universal Debug Enable/Disable

//const uint8_t jointNum = 52;             // Specific I2C address matching joint numb

#include <Wire.h>             // I2C library

int pulseWritePin = 9;        // Writes a pulse to the Stepper Driver

int enableReadPin = 10;        // Reads the Mega for movements requests

//int enableWritePin = 6;       // Pass through for movement request from Mega and Kinematics

int directionReadPin = 3;     // Reads for direction of joint Movement requests

int directionWritePin = 8;    // Pass through for direction requests from Mega and Kinematics

// Joint 1 -------------> HIGH --->(250 and 100)    LOW ----->(500 and 500)     I2C ---> 11
// Joint 4 -------------> HIGH --->(350 and 300)    LOW ----->(500 and 500)     I2C ---> 41
// Joint 5.1 -----------> HIGH --->(250 and 100)    LOW ----->(500 and 500)     I2C ---> 51
// Joint 5.2 -----------> HIGH --->(250 and 100)    LOW ----->(500 and 500)     I2C ---> 52

int currentFreq = 0;


// 31200 steps for 90 degree turn on joint 1   ( 1 ----> CW, 2 ----->CCW)
//Joint1

const uint8_t jointNum = 11;
int freqHighON = 250; int freqHighOFF = 100; //
int freqLowON = 500; int freqLowOFF = 500; //
float steps_per_deg = 346.67;



// 6500 steps for 45 degree turn on joint 4    ( 1 -----> DOWN, 2 ------> UP)
//Joint4
/*
const uint8_t jointNum = 41;
int freqHighON = 350; int freqHighOFF = 300; //
int freqLowON = 500; int freqLowOFF = 500; //
float steps_per_deg = 144.445;
*/

//Joint51
/*
const uint8_t jointNum = 51;
int freqHighON = 250; int freqHighOFF = 100; //
int freqLowON = 500; int freqLowOFF = 500; //
int steps_per_deg = 1;
*/

//Joint52
/*
const uint8_t jointNum = 52;
int freqHighON = 250; int freqHighOFF = 100; //
int freqLowON = 500; int freqLowOFF = 500; //
int steps_per_deg = 1;
*/

int freqArray[2][2] = {{freqHighON,freqHighOFF},{freqLowON,freqLowOFF}};

int sensorPin = A1;    // select the input pin for the potentiometer
  
int sensorValue = 0;  // variable to store the value coming from the sensor

void setup() {

  Serial.begin(9600);

  pinMode(enableReadPin,      INPUT);

  pinMode(directionReadPin,   INPUT);    

  pinMode(pulseWritePin,      OUTPUT);

  //pinMode(enableWritePin,     OUTPUT);

  pinMode(directionWritePin,  OUTPUT);

  //digitalWrite(enableWritePin, LOW);

  

  Wire.begin(jointNum);               // join i2c bus with the number for the attached joint

  Wire.onReceive(receiveEvent);       // register event

 

  if(debug){Serial.begin(9600);}      // start serial for output when debug is enabled

}

void loop() {

  // Checks to pass throught the Mega joint direction requests 

  if(digitalRead(directionReadPin) == HIGH)

    digitalWrite(directionWritePin, HIGH);

  else

    digitalWrite(directionWritePin, LOW);

  // Constant On pulse to drive the stepper joint motors when enablePin is HIGH

  // the freqON can be updated

  if(digitalRead(enableReadPin)){

    digitalWrite(pulseWritePin, HIGH);

    delayMicroseconds(freqArray[currentFreq][0]);

    digitalWrite(pulseWritePin, LOW);

    delayMicroseconds(freqArray[currentFreq][1]);

  }

}

// function that executes whenever data is received from master

// this function is registered as an event, see setup()

void receiveEvent(int howMany) {

  char ch[20] = {'-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-'};
  char dh[20] = {'-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-'};
  int z = 0;
 

  while (0 < Wire.available()) { // loop through all but the last
    ch[z++] = Wire.read(); // receive byte as a character
    Serial.print(ch[z-1]);         // print the character
  }

  Serial.println();
  
  char c = ch[1];          // receives the step command

  for(int i = 2; i < sizeof(ch); i++)
  {
    dh[i-2] = ch[i];
  }

  long int x = atoi(dh);            // receive byte as an integer

  x = int( x * steps_per_deg);

  if(debug){Serial.print(c); Serial.print("  "); Serial.println(x);}   // print the integer if debug enabled

  switch(c){

    case '1':{

      stepKinematics(x);     // calls the step command

      break;

    }

   case '2':{

      stepKinematics(-x);     // calls the step command

      break;

    }

   case '8':{

      currentFreq = x;      // updates the frequency of stepper pulse

      break;

    }

   case '9':{

      
      sensorValue = analogRead(sensorPin);
  
      Serial.println(sensorValue);

      char buff[3];

      sprintf(buff, "%i", sensorValue);

      Serial.print(buff);

      Wire.write(250);      // updates the frequency of stepper pulse

      break;

    }

  }                  

}

// When kinematic steps are requested then this control function will move the 

//  joint that exact amount of steps. If step count is negative then the reverse 

//  direction is requested.

void stepKinematics(int stepcount){

  // Check direction

  if(stepcount > 0)

    digitalWrite(directionWritePin, HIGH);

  else {

    digitalWrite(directionWritePin, LOW);

    stepcount *= -1;

  }

      

  //digitalWrite(enableWritePin, HIGH);       // enable the driver

  

  // Start stepping 

  for(int x = 0;x < stepcount; x++){

    digitalWrite(pulseWritePin, HIGH);

    delayMicroseconds(freqArray[currentFreq][0]);

    digitalWrite(pulseWritePin, LOW);

    delayMicroseconds(freqArray[currentFreq][1]);


  }

  //  Stop stepping

  //digitalWrite(enableWritePin, LOW);

}


