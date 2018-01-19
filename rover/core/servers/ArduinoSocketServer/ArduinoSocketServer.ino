/*
   Special Thanks goes to Joseph Porter for development of first edition 
   of the Atlas Control.  His code was heavily used in the development 
   of 2018 Atlas.
   
   Description:
    This is the control for the mobility and arm. Which runs a socket
    server to receive commands and send feedback
*/

#include <SPI.h>
//#include <Servo.h>
//#include <Stepper.h>

// Joint #1
const uint8_t joint1_pulse_pin = 2;
const uint8_t joint1_dir_pin = 6;
const uint8_t joint1_enab_pin = 31;

// Joint 4
const uint8_t joint4_pulse_pin = 3;
const uint8_t joint4_dir_pin = 7;

// Joint 5a
const uint8_t joint5a_pulse_pin = 4;
const uint8_t joint5a_dir_pin = 8;

// Joint 5b
const uint8_t joint5b_pulse_pin = 5;
const uint8_t joint5b_dir_pin = 9;


//Color Pins
int redPin = 24;
int bluePin = 26;
int greenPin = 22;

//Sabertooth Communications
#include <SoftwareSerial.h>
#include "Sabertooth.h"

//Network Sheild Ethernet2 setup
#include <SPI.h>         // needed for Arduino versions later than 0018
#include <Ethernet2.h>
#include <EthernetUdp2.h>

SoftwareSerial SWSerial(NOT_A_PIN, 1);
Sabertooth ST(128, SWSerial);
Sabertooth ARM(129, SWSerial);

int packetSize;
// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 0x90, 0xA2, 0xDA, 0x10, 0x30, 0xD3 };
byte ip[] = {192, 168, 1, 10};
byte gateway[] = {192,168,1,1};
byte subnet[] = {255,255,255,0};

// local port to listen on
unsigned int localPort = 5000;   
unsigned int localPortBaseStation = 6000;   

//Storage for Commands and Values 
char charToIntArray[10];
int moveMentArray[10];

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //buffer to hold incoming packet,
//char  ReplyBuffer[] = "acknowledged";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;
EthernetUDPBase Udp_Base;  //customize communication===========================================

// Protection from loss of communication using millis()
unsigned long interval = 500;
unsigned long previousMillis=0;

void setTheEthernetConnection() {
  Ethernet.begin(mac, ip, gateway, subnet);
  Udp.begin(localPort);
  Udp.begin(localPortBaseStation);  //Do we need this???  Should this customize communication==========================
  ledBlink(50);
}

// This function is used to blink the LED RED when lose of network occures
void ledBlink(unsigned int blinkSpeed) {
  digitalWrite(bluePin, LOW);
  digitalWrite(greenPin, LOW); 
  for(unsigned int i = 0; i < 15; ++i) {
    digitalWrite(redPin, LOW);       
    delay(blinkSpeed);
    digitalWrite(redPin, HIGH);       
    delay(blinkSpeed);
  }
}

void setup() {
  // Software Serial Setup
  SWSerial.begin(9600);
  ST.autobaud();
  ARM.autobaud();

  //****** Move this to seperate function and call it
  //Create an initalization function to reset rover to default state
  // on startup for motors and Arm
  ST.motor(1, 0);
  ST.motor(2, 0);
  ARM.motor(1, 0);
  ARM.motor(2, 0);
  
  //Serial.begin(9600);  //For debuging but will not work with SWSerial
  
  // start the Ethernet and UDP:
  //setTheEthernetConnection();
  Ethernet.begin(mac, ip, gateway, subnet);
  Udp.begin(localPort);
  Udp.begin(localPortBaseStation);
  delay(1500);
  
  // Set up Joint1
  pinMode(joint1_dir_pin, OUTPUT);
  pinMode(joint1_enab_pin, OUTPUT);
  pinMode(joint1_pulse_pin, OUTPUT);
  digitalWrite(joint1_enab_pin, LOW);

  // Set up Joint4
  pinMode(joint4_dir_pin, OUTPUT);
  pinMode(joint4_pulse_pin, OUTPUT);
  digitalWrite(joint4_dir_pin, LOW);
  digitalWrite(joint4_pulse_pin, LOW);
  
  // Set up Joint5a
  pinMode(joint5a_dir_pin, OUTPUT);
  pinMode(joint5a_pulse_pin, OUTPUT);
  
  // Set up Joint5b
  pinMode(joint5b_dir_pin, OUTPUT);
  pinMode(joint5b_pulse_pin, OUTPUT);


  // setup the output pins for each color LED
  pinMode(redPin, OUTPUT);  
  pinMode(bluePin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  
}

// This loop will be a command loop for each of the arduino processes
void loop() {
  //Receives the Array of Commands and Values
  packetSize = Udp.parsePacket();
  
  //Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  //Udp.write('r');  //Change this to const array = ready
  //Udp.endPacket();

  //memset(packetBuffer,0,sizeof(UDP_TX_PACKET_MAX_SIZE));
  //debug
  //Serial.println(Udp.remoteIP());
  //Serial.println(Udp.remotePort());
  
  //If no network traffic then the rover will stop
  if((unsigned int)(millis() - previousMillis) > interval){
    ST.drive(0);
    ST.turn(0);
    ARM.motor(1,0);
    ARM.motor(2,0);
    ledBlink(100);
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write('r');  //Change this to const array = ready
    Udp.endPacket();
    //setTheEthernetConnection();
  }

  // NOT SURE WHY I INCLUDED THIS AT THE MOMENT
  Udp.write(packetBuffer, UDP_TX_PACKET_MAX_SIZE);

  //Restricts the access to only when receiving network comm
  if (packetSize) {
    previousMillis = millis();    // Stores current time for check outside of loop
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //reads the packet
    // parse statement for packetBuffer to Control Array
    // x controls buffer place, y controls current char read, 
    //    n controls placement in array 
    //    The Array is comma delimited
    for(int x,y,n = 0; x < packetSize; x++, y++){
      charToIntArray[y] = packetBuffer[x];

      //  Parses at comma and stores the value read in n array place
      if(charToIntArray[y] == ','){
        charToIntArray[y] = '\0';
        moveMentArray[n++] = atoi(charToIntArray);
        y = -1;
        memset(charToIntArray,0,sizeof(charToIntArray));  // clear mem
      }
      //  Catch if no more values to receive
      else if(x + 1 == packetSize){
        charToIntArray[++y] = '\0';
        moveMentArray[n++] = atoi(charToIntArray);
        y = -1;
        memset(charToIntArray,0,sizeof(charToIntArray));  // clear mem
      }
    }
    // Loop the array and match to case and apply the values
    for(int x = 0; x < 10; x++){
      switch (x){
        // drive speed
        case 0: 
        {
          ST.drive(moveMentArray[0]);
          //Serial.println(moveMentArray[0]);
          break;
        }
        // Turning Rate
        case 1:{
          ST.turn(moveMentArray[1]);
          //Serial.println(moveMentArray[1]);
          break;  
        }
        //////////////////////////////////// 
        /*case 2 - 8: // Arm*/
        case 2:{
          ARM.motor(1,moveMentArray[2]);
          break;
        }
        case 3:{
          ARM.motor(2,moveMentArray[3]);  
          break;
        }
        case 4:{  //Joint 1
          if(moveMentArray[4] == -1 || moveMentArray[4] == 1){
            digitalWrite(joint1_pulse_pin,HIGH);
            if(moveMentArray[4] == 1){
              digitalWrite(joint1_dir_pin,HIGH);
            }
            else{
              digitalWrite(joint1_dir_pin,LOW);
            }
          }
          else{
            digitalWrite(joint1_pulse_pin,LOW);
          }
          break;
        }
        case 5:{  //Joint 4
          if(moveMentArray[5] == -1 || moveMentArray[5] == 1){
            digitalWrite(joint4_pulse_pin,HIGH);
            if(moveMentArray[5] == 1){
              digitalWrite(joint4_dir_pin,HIGH);
            }
            else{
              digitalWrite(joint4_dir_pin,LOW);
            }
          }
          else{
            digitalWrite(joint4_pulse_pin,LOW);
          }
          break;
        }
        case 6:{  //Joint 5a
          if(moveMentArray[6] == -1 || moveMentArray[6] == 1){
            digitalWrite(joint5a_pulse_pin,HIGH);
            if(moveMentArray[6] == 1){
              digitalWrite(joint5a_dir_pin,HIGH);
            }
            else{
              digitalWrite(joint5a_dir_pin,LOW);
            }
          }
          else{
            digitalWrite(joint5a_pulse_pin,LOW);
          }
          break;
        }
        case 7:{  //Joint 5b
          if(moveMentArray[7] == -1 || moveMentArray[7] == 1){
            digitalWrite(joint5b_pulse_pin,HIGH);
            if(moveMentArray[7] == 1){
              digitalWrite(joint5b_dir_pin,HIGH);
            }
            else{
              digitalWrite(joint5b_dir_pin,LOW);
            }
          }
          else{
            digitalWrite(joint5b_pulse_pin,LOW);
          }
          break;
        }
        case 9:
              {                
                //Switch on the LEDs as per the array input number 9
                switchLEDs(moveMentArray[9]);
                Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
                //consider instead of 'r' and 'r 1' and 1 is logging message for all OK functions
                Udp.write('r');  //Change this to const array = ready
                Udp.endPacket();

                memset(packetBuffer,0,sizeof(UDP_TX_PACKET_MAX_SIZE));
                                
                break;
              }

        
        ////////////////////////////////////

        ////////////////////////////////////
        //case 7:     // reset Command
        //
        //  runs the reset function


        ////////////////////////////////////
      }  
    }

    

    //Sends the ready command asking for next transmittion
    //Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    //Udp.write('r');  //Change this to const array = ready
    //Udp.endPacket();
  }         
  //clears the buffer to ensure all new values
  memset(packetBuffer,0,sizeof(UDP_TX_PACKET_MAX_SIZE));
}


// Will switch the pin based on what byte is sent from the pi
void setDirectionPin(uint8_t pinValue, uint8_t val)
{
  if (val == 0x00)
  {
    digitalWrite(pinValue, LOW);
  }
  else if (val == 0x01)
  {
    digitalWrite(pinValue, HIGH);
  }
}

void Step_Joint(int step1, int pulse_pin, int dir_pin, int dir ){
  ST.drive(0);
  ST.turn(0);
  digitalWrite(dir_pin, dir);
  for(int x = 0; x < step1; x++){
    digitalWrite(pulse_pin, HIGH);
    digitalWrite(pulse_pin, LOW);
    delay(1);
  }
}



//takes color code as input, and lights the corresponding LED
void switchLEDs(int colorCode) {
  switch(colorCode)
  {
    case 0:
        //Red
        digitalWrite(redPin, HIGH);       
        digitalWrite(bluePin, LOW);
        digitalWrite(greenPin, LOW);            
        
        break;            
    case 1:
        //Green
        digitalWrite(greenPin, HIGH);
        digitalWrite(bluePin, LOW);
        digitalWrite(redPin, LOW);            
        
        break;    
    case 2:
        //Blue
        digitalWrite(bluePin, HIGH);
        digitalWrite(redPin, LOW);            
        digitalWrite(greenPin, LOW);
            
        break;
            
    case 3:
        //Purple
        digitalWrite(redPin, HIGH);
        digitalWrite(bluePin, HIGH);
        digitalWrite(greenPin, LOW);
            
        break;  
  }  
}
