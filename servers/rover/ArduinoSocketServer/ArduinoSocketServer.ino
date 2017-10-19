/*
   Special Thanks goes to Joseph Porter for development of first edition 
   of the Atlas Control.  His code was heavily used in the development 
   of 2018 Atlas.
   
   Description:
    This is the control for the mobility and arm. Which runs a socket
    server to receive commands and send feedback
*/

#include <SPI.h>
//#include <AMIS30543.h>
#include <Servo.h>
#include <Stepper.h>
//#include <TimerOne.h>

const int stepsPerRevolution = 200;
// X Axis Mobility
/*Servo x_mobility;
  const uint8_t x_pwm_pin = 6;

  // Y Axis Mobility
  Servo y_mobility;
  const uint8_t y_pwm_pin = 7;*/

// Joint #1
const uint8_t joint1_dir_pin = 23;
const uint8_t joint1_enab_pin = 31;
const uint8_t joint1_pulse_pin = 11;

//volatile bool joint1_on = false;
//const uint8_t joint1_limit_pin = A0;
//unsigned int joint1_sensorValue;
//uint8_t joint1_bit;
//uint8_t joint1_port;
//const int upperLimit = 630;
//const int lowerLimit = 55;
//const int middlePoint = 346;
//volatile bool centerJoint1 = false;
//
//// Joint #2
//Servo joint2;
//const uint8_t joint2_pwm_pin = 4;
//
//// Joint #3
//Servo joint3;
//const uint8_t joint3_pwm_pin = 5;
//
//// Joint #4
//const uint8_t joint4_dir_pin = 32;
//const uint8_t joint4_enab_pin = 35;
//const uint8_t joint4_pulse_pin = 36;
//volatile bool joint4_on = false;
//volatile bool joint4_interrupted = false;
//volatile bool joint4_needsStepOff = false;
//const uint8_t joint4_interrupt_pin = 3;
//unsigned long joint4_TotalSteps = 0;
//uint8_t joint4_bit;
//uint8_t joint4_port;
//const unsigned long joint4_StepsLimit = 7330;
//bool joint4passedLimit = false;
//const int joint4_LimitDistance_Steps = 100;
//
//// Joint #5
const uint8_t joint5_dir_pin = 27;
//const uint8_t joint5_enab_pin = 39;
const uint8_t joint5_pulse_pin = 26;
//volatile bool joint5_on = false;
//volatile bool joint5_interrupted = false;
//volatile bool joint5_needsStepOff = false;
//const uint8_t joint5_interrupt_pin = 2;
//unsigned long joint5_TotalSteps = 0;
//uint8_t joint5_bit;
//uint8_t joint5_port;
//const unsigned long joint5_StepsLimit = 50500;
//bool joint5passedLimit = false;
//const int joint5_LimitDistance_Steps = 1000;
//
//// Joint #6
//AMIS30543 joint6_stepper;
//const uint8_t joint6_ss = 44;
//const uint8_t joint6_dir_pin = 42;
//const uint8_t joint6_pulse_pin = 43;
//volatile bool joint6_on = false;
//
//// Joint #7
//AMIS30543 joint7_stepper;
//const uint8_t joint7_ss = 48;
const uint8_t joint7_dir_pin = 25;
const uint8_t joint7_pulse_pin = 24;
//volatile bool joint7_on = false;
//
//// AssAss globals
//Servo AssAss;
//const uint8_t assass_pwm_pin = 9;

// Additional Global variables needed
uint8_t val[6];
int i;
int delayVal = 1;
uint16_t pwmVal;
const int interruptDelay = 350;
const int ignoreDelay = 250;
static unsigned long ignore_time = 0;
static unsigned long last_interrupt_time = 0;

bool Calibrated = false;  // Arm can't be moved until calibrated
bool debug = false;
bool ignoreLimit = true;
uint8_t analogRead_counter = 0;



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
byte ip[] = {192, 168, 1, 177};
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

// Protection from loss of communication using millis()
unsigned long interval = 500;
unsigned long previousMillis=0;

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
  Ethernet.begin(mac, ip, gateway, subnet);
  Udp.begin(localPort);
  Udp.begin(localPortBaseStation);

  delay(1500); //give a sec to start process

  // Set up Joint1
  pinMode(joint1_dir_pin, OUTPUT);
  pinMode(joint1_enab_pin, OUTPUT);
  pinMode(joint1_pulse_pin, OUTPUT);
  digitalWrite(joint1_enab_pin, LOW);

  // Set up Joint1
  pinMode(joint5_dir_pin, OUTPUT);
  //pinMode(joint5_enab_pin, OUTPUT);
  pinMode(joint5_pulse_pin, OUTPUT);
  //digitalWrite(joint5_enab_pin, LOW);

  // Set up Joint1
  pinMode(joint7_dir_pin, OUTPUT);
  //pinMode(joint7_enab_pin, OUTPUT);
  pinMode(joint7_pulse_pin, OUTPUT);
  //digitalWrite(joint7_enab_pin, LOW);


  
}
// This loop will be a command loop for each of the arduino processes
void loop() {
  //Receives the Array of Commands and Values
  packetSize = Udp.parsePacket();
  
  //debug
  //Serial.println(Udp.remoteIP());
  //Serial.println(Udp.remotePort());
  
  //If no network traffic then the rover will stop
  if((unsigned int)(millis() - previousMillis) > interval){
    ST.drive(0);
    ST.turn(0);
    ARM.motor(1,0);
    ARM.motor(2,0);
  }

  // NOT SURE WHY I INCLUDED THIS AT THE MOMENT
  Udp.write(packetBuffer, UDP_TX_PACKET_MAX_SIZE);

  //Restricts the access to only when receiving network comm
  if (packetSize) {
    previousMillis = millis();    // Stores current time for check outside of loop
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //reads the packet 
    //Serial.println(packetBuffer);
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
    for(int x = 0; x < 5; x++){
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
        case 4:{
          if(moveMentArray[4]){
            ST.drive(0);
            ST.turn(0);
            Step_Joint(200,joint1_pulse_pin, joint1_dir_pin, moveMentArray[5]);
          }
          break;
        }
        case 5:{
          if(moveMentArray[6]){
            ST.drive(0);
            ST.turn(0);
            Step_Joint(200,joint1_pulse_pin, joint1_dir_pin, moveMentArray[7]);
          }
          break;
        }
        case 6:{
          if(moveMentArray[8] or moveMentArray[9]){
            if(moveMentArray[8]){
              Step_Joint(100, joint7_pulse_pin, joint7_dir_pin, 0);  
            }
            else
              Step_Joint(100, joint7_pulse_pin, joint7_dir_pin, 1);
          }
          break;
        }
                
        ////////////////////////////////////

        ////////////////////////////////////
        //case 10:     // reset Command
        //
        //  runs the reset function


        ////////////////////////////////////
      }  
    }

    //Sends the ready command asking for next transmittion
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write("ready");  //Change this to const array = ready
    Udp.endPacket();
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
  digitalWrite(dir_pin, dir);
  for(int x = 0; x < step1; x++){
    digitalWrite(pulse_pin, HIGH);
    digitalWrite(pulse_pin, LOW);
    delay(1);
  }
}

