
#include <SPI.h>
#include <Servo.h>
#include <Stepper.h>
#include <SoftwareSerial.h>
#include "AMIS30543\AMIS30543.h"
//include "Sabertooth\Sabertooth\Sabertooth.h"
/*
/////// Const and Variables /////////////
const int stepsPerRevolution = 200;
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

/////////// Joint 1 /////////////
    const uint8_t joint1_dir_pin = 30;
    const uint8_t joint1_enab_pin = 31;
    const uint8_t joint1_pulse_pin = 29;
    volatile bool joint1_on = false;
    const uint8_t joint1_limit_pin = A0;
    unsigned int joint1_sensorValue;
    uint8_t joint1_bit;
    uint8_t joint1_port;
    const int upperLimit = 630;
    const int lowerLimit = 55;
    const int middlePoint = 346;
    volatile bool centerJoint1 = false;
  /////////// Joint 2 /////////////
    Servo joint2;
    const uint8_t joint2_pwm_pin = 4;
  /////////// Joint 3 /////////////
    Servo joint3;
    const uint8_t joint3_pwm_pin = 5;
  /////////// Joint 4 /////////////
    const uint8_t joint4_dir_pin = 32;
    const uint8_t joint4_enab_pin = 35;
    const uint8_t joint4_pulse_pin = 36;
    volatile bool joint4_on = false;
    volatile bool joint4_interrupted = false;
    volatile bool joint4_needsStepOff = false;
    const uint8_t joint4_interrupt_pin = 3;
    unsigned long joint4_TotalSteps = 0;
    uint8_t joint4_bit;
    uint8_t joint4_port;
    const unsigned long joint4_StepsLimit = 7330;
    bool joint4passedLimit = false;
    const int joint4_LimitDistance_Steps = 100;
  /////////// Joint 5 /////////////
    const uint8_t joint5_dir_pin = 38;
    const uint8_t joint5_enab_pin = 39;
    const uint8_t joint5_pulse_pin = 40;
    volatile bool joint5_on = false;
    volatile bool joint5_interrupted = false;
    volatile bool joint5_needsStepOff = false;
    const uint8_t joint5_interrupt_pin = 2;
    unsigned long joint5_TotalSteps = 0;
    uint8_t joint5_bit;
    uint8_t joint5_port;
    const unsigned long joint5_StepsLimit = 50500;
    bool joint5passedLimit = false;
    const int joint5_LimitDistance_Steps = 1000;
  /////////// Joint 6 /////////////
    //AMIS30543 joint6_stepper;
    const uint8_t joint6_ss = 44;
    const uint8_t joint6_dir_pin = 42;
    const uint8_t joint6_pulse_pin = 43;
    volatile bool joint6_on = false;
  /////////// Joint 7 /////////////
    //AMIS30543 joint7_stepper;
    const uint8_t joint7_ss = 48;
    const uint8_t joint7_dir_pin = 46;
    const uint8_t joint7_pulse_pin = 47;
    volatile bool joint7_on = false;

//SoftwareSerial SWSerial(NOT_A_PIN, 18); // tx-1 on arduino mega
//Sabertooth Back(129, Serial1);
*/
/////// Taranis Variables start ////////
unsigned long int startTime,endTime,deltaTime;
volatile int ppmIN[18],buffer_arr[18],iterator ,global_Array[8];
//specifing arrays and variables to store values 
/////// Taranis Variables end   ////////

void setup() {
  //////// Taranis Setup /////////////
  // enabling interrupt at pin 2
    pinMode(2, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(2), read_me, RISING);
  //initialize the counter
    iterator = 0;
  //////// Taranis End   /////////////
  for(int x = 3; x < 13; x++)
    pinMode(x, OUTPUT);
  SPI.begin();
  //Serial.begin(9600);
  Serial1.begin(9600);
  //Back.autobaud();

  delay(5);
/*
  //Back.drive(0);
  Back.turn(0);
  
  joint1_sensorValue = analogRead(joint1_limit_pin);

  // Setup the linear actuators
  joint2.attach(joint2_pwm_pin);
  joint2.writeMicroseconds(1500);

  joint3.attach(joint3_pwm_pin);
  joint3.writeMicroseconds(1500);

  // Set up Joint1
  pinMode(joint1_dir_pin, OUTPUT);
  pinMode(joint1_enab_pin, OUTPUT);
  pinMode(joint1_pulse_pin, OUTPUT);
  digitalWrite(joint1_enab_pin, LOW);

  // Set up Joint4
  pinMode(joint4_dir_pin, OUTPUT);
  pinMode(joint4_enab_pin, OUTPUT);
  pinMode(joint4_pulse_pin, OUTPUT);
  pinMode(joint4_interrupt_pin, INPUT);
  //attachInterrupt(digitalPinToInterrupt(joint4_interrupt_pin), stopJoint4, FALLING);
  digitalWrite(joint4_enab_pin, LOW);

  // Set up Joint5
  pinMode(joint5_dir_pin, OUTPUT);
  pinMode(joint5_enab_pin, OUTPUT);
  pinMode(joint5_pulse_pin, OUTPUT);
  pinMode(joint5_interrupt_pin, INPUT);
  //attachInterrupt(digitalPinToInterrupt(joint5_interrupt_pin), stopJoint5, FALLING);
  digitalWrite(joint5_enab_pin, LOW);

  // Set up the Polulu Stepper motors
  //joint6_stepper.init(joint6_ss);
  //joint6_stepper.resetSettings();
  //joint6_stepper.setCurrentMilliamps(670);
  //joint6_stepper.setStepMode(stepsPerRevolution);
  //joint6_stepper.enableDriver();

  // Deselect the slave select pin for joint6 to allow joint7 to communicate
  //digitalWrite(joint6_ss, HIGH);

  //joint7_stepper.init(joint7_ss);
  //joint7_stepper.resetSettings();
  //joint7_stepper.setCurrentMilliamps(1250);
  //joint7_stepper.setStepMode(stepsPerRevolution);
  //joint7_stepper.enableDriver();

  // Set up AssAss
  //AssAss.attach(assass_pwm_pin);

  // Arduino needs these functions to be wrapped in another function
  // This will set certain masks that allow use to detect the HIGH LOW of a pin faster
  //setPortandBit();
  
  */
}

void loop() {
  ////// Taranis Start ///////
  read_Array();
  //For debugging if needed
  for(int b = 0; b < 8; b++){
    //Serial.print(global_Array[b]);
    //Serial.print("\t");
    if(global_Array[b] > 1600){
      switch(b){
        case 0:{
          digitalWrite(3, HIGH);
          break;
        }
        case 1:{
          digitalWrite(5, HIGH);
          break;
        }
        case 2:{
          digitalWrite(7, HIGH);
          break;
        }
        case 3:{
          digitalWrite(9, HIGH);
          break;
        }
        case 4:{
          digitalWrite(11, HIGH);
          break;
        }
      }
    }
    else if(global_Array[b] < 1400){
      switch(b){
        case 0:{
          digitalWrite(4, HIGH);
          break;
        }
        case 1:{
          digitalWrite(6, HIGH);
          break;
        }
        case 2:{
          digitalWrite(8, HIGH);
          break;
        }
        case 3:{
          digitalWrite(10, HIGH);
          break;
        }
        case 4:{
          digitalWrite(12, HIGH);
          break;
        }
      }
    }
    else {
      switch(b){
        case 0:{
          digitalWrite(3, LOW);
          digitalWrite(4, LOW);
          break;
        }
        case 1:{
          digitalWrite(5, LOW);
          digitalWrite(6, LOW);
          break;
        }
        case 2:{
          digitalWrite(7, LOW);
          digitalWrite(8, LOW);
          break;
        }
        case 3:{
          digitalWrite(9, LOW);
          digitalWrite(10, LOW);
          break;
        }
        case 4:{
          digitalWrite(11, LOW);
          digitalWrite(12, LOW);
          break;
        }
      }
    }  
  }
  Serial.print("\n");
  delay(100);
  ////// Taranis End ///////
  
}


////////////read_me() Taranis Funct //////////////////////////////////////////////////////////////////
//  
//  INPUT - Global arrays for fetching, buffering, retreival(before next iteration)
//  OUTPUT - Global array filled with PPM signals 
//  This code reads 2 sets of values from RC reciever of PPM signals on Pin 2.  It will then store them 
//    in another array to allow the software to continue without interfering with the interrupt calls.
//
//////////////////////////////////////////////////////////////////////////////////////////////////////
void read_me()  {
         
  startTime=micros();           // store time value a when pin value falling
  deltaTime=startTime-endTime;  // calculating time inbetween two peaks
  endTime=startTime;            // delta time of PPM signal
  ppmIN[iterator++]=deltaTime;             // storing 15 value in array
  
  //iterator++;       
  if(iterator==18){
    for(int j=0;j<18;j++){
      buffer_arr[j]=ppmIN[j];
    }
    iterator=0;
  }
}

////////////read_Array() Taranis Funct ///////////////////////////////////////////////////////////////
//  
//  INPUT - Global array of next iteration
//  OUTPUT - Global array filled with PPM signals 
//  
//
//////////////////////////////////////////////////////////////////////////////////////////////////////
void read_Array(){
  int iteration = 0;
  int startPoint = 0;
  int ppmGap = 0;
  for( ppmGap = 9; ppmGap > -1; ppmGap-- )
    if(buffer_arr[ppmGap]>3000){
      startPoint = ppmGap;  //detecting separation space 10000us in that another array                     
      break;
    }
  for(iteration=0; iteration<8; iteration++){
    global_Array[iteration]=buffer_arr[++startPoint];  //assign 6 channel values after separation space
  }
}
