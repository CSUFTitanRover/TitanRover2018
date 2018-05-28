#define buflen 4 //size of the data to be read, in bytes

int pinDirection = 5; //DIR+

int pinPulse = 7; //PUL+

int pinEnable = 9;//ENA+

int pinAnalog = A0;//POT DATA (black right now)

float heading;//

float newheading;

void *myptr;

char ayte[buflen];

int y = 0;

long temp;

int pot;//value to store potentiometer reading

void setup() {
  
  Serial.begin(9600);
  
  Serial.setTimeout(4294967295); //maximum time allowed for sleep
  
  pinMode(pinAnalog, INPUT);
  
  pinMode(pinDirection, OUTPUT);
  
  pinMode(pinPulse, OUTPUT);
  
  pinMode(pinEnable, OUTPUT);
  
  digitalWrite(pinEnable, LOW); //Allows driver to be controlled
  
  pot = analogRead(pinAnalog); 
  
  backtoStart(); //See bottom of file, rotates antennae to initalization position

//  Serial.println("About to read buffer data");

//  Serial.println(pot);

//  Serial.readBytes(ayte, buflen);

  myptr = ayte;

  temp = *((long*)myptr); //casting the voidpointer to a long, expecting an int, but because arduino stores ints in 2 bytes, here we are

//  Serial.println(temp);

  heading = temp/1000.; //converting the long to a float
}


void loop() 
{

  pot = analogRead(pinAnalog);

//  Serial.println(pot);

  if(pot > 768 || pot < 256) //Acceptable ranges, corresponds to +/- 151.58 degrees
  {
    backtoStart();
  } 
  
  Serial.readBytes(ayte, buflen);
  
  myptr = ayte;
  
  temp = *((long*)myptr);
  
  newheading = temp/1000.;
  
//  Serial.println("About to take a step!");
  
//  Serial.println(newheading);
  
//  Serial.println(heading);
  
//  Serial.println(heading - newheading);
  
//  Serial.println((heading - newheading)*(76./45.));
  
//  Serial.println(pot - ((heading - newheading)*(76/45)));
  
  if(((pot - ((heading - newheading)* (76./45.))) < 256 )||((pot - ((heading - newheading)*(76./45.))) > 768))
  
  //76/45 represents a change in potentiometer reading of 76 when the main gear spins 45 degrees
  //the subtraction is due to that fact that to increase the potentiometer reading, you must lower your heading - turn counterclockwise
  //meaning ser direction to LOW
  
  {  
    Serial.println("Failed to turn");
  }
  
  else
  {
//    Serial.println("About to take");
  
//    Serial.println(heading - newheading);
   
//    Serial.println("steps");
   
//    delay(1000);
   
    takeSteps(heading - newheading);
   
//    Serial.println(heading);
   
    heading = newheading;
  }
  
//  Serial.println(heading);
}
//arguments: angle change needed, in degrees
//outputs: steps taken as an int
//what it does: makes the motor perform necessary number of steps
//assumptions: 4.25:1 gearbox on motor, 6:1 large gear to motor gear
//microsteps = 2, and base step angle of 1.8 
//(this is where the 1.8/51 comes from)

void takeSteps(float degree)
{
  if(degree > 0 && degree < 150)
  {
    for(y = 0;y < (degree/(1.8/51));y++)
    {
 
      digitalWrite(pinDirection, LOW);//clockwise

      digitalWrite(pinPulse, HIGH);

      delayMicroseconds(500);

      digitalWrite(pinPulse, LOW);

      delayMicroseconds(500);

      Serial.println(y);

    }
  }
  else if(degree < 0 && degree > -150)
  {
    for(y = 0;y < -1* (degree/(1.8/51));y++)
      {
 
        digitalWrite(pinDirection, HIGH);//counterclockwise

        digitalWrite(pinPulse, HIGH);
     
        delayMicroseconds(500);
     
        digitalWrite(pinPulse, LOW);
     
        delayMicroseconds(500);
     
        Serial.println(y);
      
     }
  }
}
void backtoStart(){
 
  if(pot > 514)
  {
    for(;analogRead(pinAnalog) > 514;)
    {
 
      digitalWrite(pinEnable, LOW);
    
      digitalWrite(pinDirection, LOW);
    
      digitalWrite(pinPulse, HIGH);
    
      delayMicroseconds(500);
    
      digitalWrite(pinPulse, LOW);
    
      delayMicroseconds(500);
    
      Serial.println(analogRead(pinAnalog));
    
    }  
 }
  else if(analogRead(pinAnalog) < 510)
  {
  
    for(;analogRead(pinAnalog) <  510;)
    {
    
      digitalWrite(pinEnable, LOW);
    
      digitalWrite(pinDirection, HIGH);
    
      digitalWrite(pinPulse, HIGH);
    
      delayMicroseconds(500);
    
      digitalWrite(pinPulse, LOW);
    
      delayMicroseconds(500);
    
      Serial.println(analogRead(pinAnalog));
    
    }  
  } 
}
