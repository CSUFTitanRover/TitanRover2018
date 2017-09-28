#include <SPI.h>
#include <Servo.h>
#include <Stepper.h>
#include <SoftwareSerial.h>
#include "AMIS30543\AMIS30543.h"
#include "Sabertooth\Sabertooth\Sabertooth.h"

/////// Const and Variables /////////////
//const int stepsPerRevolution = 200;
//uint8_t val[6];
//int i;
//int delayVal = 1;
//uint16_t pwmVal;
//const int interruptDelay = 350;
//const int ignoreDelay = 250;
//static unsigned long ignore_time = 0;
//static unsigned long last_interrupt_time = 0;

//bool Calibrated = false;  // Arm can't be moved until calibrated
//bool debug = false;
//bool ignoreLimit = true;
//uint8_t analogRead_counter = 0;
/////////// Taranis Globals /////////////
    const uint8_t taranis_interrupt_pin = 2;

/////////// Joint 1 /////////////   http://www.stevenrhine.com/wp-content/uploads/2015/10/Sumtor-Elec-MB450A-Manual-English.pdf
    const uint8_t joint1_dir_pin = 30;
    const uint8_t joint1_enab_pin = 31;
    const uint8_t joint1_pulse_pin = 29;
    volatile bool joint1_on = false;
    const uint8_t joint1_limit_pin = A0;
    unsigned int joint1_sensorValue;   //location of joint
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
  /////////// Joint 4 /////////////  http://www.stevenrhine.com/wp-content/uploads/2015/10/Sumtor-Elec-MB450A-Manual-English.pdf
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
  /////////// Joint 5 /////////////  http://www.stevenrhine.com/wp-content/uploads/2015/10/Sumtor-Elec-MB450A-Manual-English.pdf
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

SoftwareSerial MotorSerial(NOT_A_PIN, 18); // tx-1 on arduino mega
SoftwareSerial ARMSerial(NOT_A_PIN, 16); // tx-1 on arduino mega
Sabertooth Motor(129, MotorSerial);
Sabertooth ARM(129, ARMSerial);

/////// Taranis Variables start ////////
unsigned long int startTime,endTime,deltaTime;
volatile int ppmIN[27],buffer_arr[27],iterator ,global_Array[16];
//specifing arrays and variables to store values 
/////// Taranis Variables end   ////////

void setup() {
  //////// Taranis Setup /////////////
  // enabling taranis_interrupt_pin
    pinMode(taranis_interrupt_pin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(taranis_interrupt_pin), PPM_reader, RISING);
    int testVal = 0;
  //initialize the counter
    iterator = 0;
  //////// Taranis End   /////////////
  
  //////// LED Testing ///////////////
  ///////////////////////////////////
  
  SPI.begin();
  Serial.begin(9600);
  MotorSerial.begin(9600);
  ARMSerial.begin(9600);
  Motor.autobaud();
  ARM.autobaud();
  
  delay(5);

  Motor.drive(0);
  Motor.turn(0);

  ARM.drive(0);
  ARM.turn(0);
  
  //joint1_sensorValue = analogRead(joint1_limit_pin);

  // Setup the linear actuators
  //joint2.attach(joint2_pwm_pin);
  //joint2.writeMicroseconds(1500);

  //joint3.attach(joint3_pwm_pin);
  //joint3.writeMicroseconds(1500);

  // Set up Joint1
//  pinMode(joint1_dir_pin, OUTPUT);
//  pinMode(joint1_enab_pin, OUTPUT);
//  pinMode(joint1_pulse_pin, OUTPUT);
//  digitalWrite(joint1_enab_pin, LOW);
/*
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
*/
  // Set up AssAss
  //AssAss.attach(assass_pwm_pin);

  // Arduino needs these functions to be wrapped in another function
  // This will set certain masks that allow use to detect the HIGH LOW of a pin faster
  //setPortandBit();
  
  //Rover_Calibration();
}

void loop() {
  ////// Taranis Start ///////
  read_Array();
  ////// Taranis End /////////
  
  for(int b = 0; b < 8; b++){
    ////  Debuging  OUTPUT
    //Serial.print(map(global_Array[b], 900, 2050, -127, 127));
    //Serial.print("\t");
    Serial.print(global_Array[b]);
    Serial.print("\t");
    Serial.println(global_Array[b+9]);
    if(abs(global_Array[b]-global_Array[b+9]) < 100){

      //map value for microsecond up down movement
      
      if(global_Array[b] >= 1600){  //High value of forward or right
        switch(b){
          //activate joints 2 and 3
          case 0:{
            ARM.drive(0);//map(global_Array[b], 990, 2050, -127, 127));
            ARM.turn(0);//map(global_Array[b], 990, 2050, -127, 127));
            //joint2.writeMicroseconds(map(global_Array[b], 990, 2050, 1000, 2000));
            //joint3.writeMicroseconds(map(global_Array[b], 990, 2050, 1000, 2000));
            //Serial.print("Arm 1 & 2 ");
            //Serial.print(map(global_Array[b], 900, 2050, -127, 127));
            //Serial.print("\t");
            //Serial.print(map(global_Array[b], 900, 2050, -127, 127));
            //Serial.print("\t");
            break;
          }
          //activate joint 1 base rotation, Counter High Clockwise Low
          case 1:{
  //          digitalWrite(joint1_enab_pin, HIGH);
  //          digitalWrite(joint1_pulse_pin, HIGH);
  //          if(joint1_limit_pin < upperLimit){
  //            digitalWrite(joint1_dir_pin, HIGH);
  //            digitalWrite(joint1_pulse_pin, HIGH);
  //          }
  //          else{
  //            digitalWrite(joint1_dir_pin, LOW);
  //            digitalWrite(joint1_pulse_pin, HIGH);
  //            delay(1000);
  //            digitalWrite(joint1_enab_pin, LOW);
  //          }
            break;
          }
          // Y-Direction on ESC
          case 2:
          // X-Direction on ESC
          case 3:{
            //communicate with ESC for x and y direction
            Motor.motor(1,map(global_Array[b], 990, 2050, -127, 127));
            Motor.motor(2,map(global_Array[b], 990, 2050, -127, 127));
            Serial.println("motor");
  //          Serial.print("Motor X & Y ");
  //          Serial.print(map(global_Array[b], 900, 2050, -127, 127));
  //          Serial.print("\t");
  //          Serial.print(map(global_Array[b+1], 900, 2050, -127, 127));
  //          Serial.print("\t");
            break;
          }
          //activate joint 2 
          case 4:{
            
            break;
          }
          //activate joint 3 
          case 5:{
            ARM.drive(0);//map(global_Array[b], 990, 2050, -127, 127));
            break;
          }
          //activate joint 4
          case 6:{
            ARM.turn(0);//map(global_Array[b], 990, 2050, -127, 127));
            break;
          }
          //activate joint 6
          case 7:{
            
            break;
          }
        }
      }
      else if(global_Array[b] <= 1400){
        switch(b){
          //activate joints 2 and 3
          case 0:{
            ARM.drive(0);//map(global_Array[b], 990, 2050, -127, 127));
            ARM.turn(0);//map(global_Array[b], 990, 2050, -127, 127));
            //joint2.writeMicroseconds(map(global_Array[b], 990, 2050, 1000, 2000));
            //joint3.writeMicroseconds(map(global_Array[b], 990, 2050, 1000, 2000));
  //          Serial.print("Arm 1 & 2 ");
  //          Serial.print(map(global_Array[b], 900, 2050, -127, 127));
  //          Serial.print("\t");
  //          Serial.print(map(global_Array[b], 900, 2050, -127, 127));
  //          Serial.print("\t");
            break;
          }
          //activate joint 1 base rotation
          case 1:{
  //          digitalWrite(joint1_enab_pin, HIGH);
  //          if(joint1_limit_pin > lowerLimit){
  //            digitalWrite(joint1_dir_pin, LOW);
  //            digitalWrite(joint1_pulse_pin, HIGH);
  //          }
  //          else{
  //            digitalWrite(joint1_dir_pin, HIGH);
  //            digitalWrite(joint1_pulse_pin, HIGH);
  //            delay(1000);
  //            digitalWrite(joint1_enab_pin, LOW);
  //          } 
            break;
          }
          // Y-Direction on ESC
          case 2:
          // X-Direction on ESC
          case 3:{
            Motor.turn(0);//map(global_Array[b], 990, 2050, -127, 127));
            Motor.drive(0);//map(global_Array[b], 990, 2050, -127, 127));
            //communicate with ESC for x and y direction
            //ST.turn(map(global_Array[b], 990, 2050, -127, 127));
            //ST.drive(map(global_Array[b+1], 990, 2050, -127, 127));
  //          Serial.print("Motors X & Y");
  //          Serial.print(map(global_Array[b], 900, 2050, -127, 127));
  //          Serial.print("\t");
  //          Serial.print(map(global_Array[b+1], 900, 2050, -127, 127));
  //          Serial.print("\t");
            break;
          }
          //activate joint 2 
          case 4:{
            
            break;
          }
          //activate joint 3 
          case 5:{
            ARM.drive(0);//map(global_Array[b], 990, 2050, -127, 127));
            break;
          }
          //activate joint 4
          case 6:{
            ARM.turn(0);//map(global_Array[b], 990, 2050, -127, 127));
            break;
          }
          //activate joint 6
          case 7:{
            
            break;
          }
        }
      }
      else {
        switch(b){
          //disable joints 2 and 3
          case 0:{
            ARM.drive(0);
            ARM.turn(0);
            break;
          }
          //activate joint 1 base rotation
          case 1:{
  //          digitalWrite(joint1_enab_pin, LOW);
  //          break;
          }
          // Y-Direction on ESC
          case 2:
          // X-Direction on ESC
          case 3:{
            //communicate with ESC for x and y direction
            //ST.turn(0);
            //ST.drive(0);
  //          Serial.print("Drive motors OFF ");
  //          break;
          }
          //activate joint 2 
          case 4:{
            
            break;
          }
          //activate joint 3 
          case 5:{
            ARM.drive(0);
            break;
          }
          //activate joint 4
          case 6:{
            ARM.turn(0);
            break;
          }
          //activate joint 6
          case 7:{
            //joint6_on = false;
            break;
          }
        }
      }  
    }
  }
  //Serial.println();
}
////////////Rover_Calibration() //////////////////////////////////////////////////////////////////
//  
//  INPUT - NONE
//  OUTPUT - NONE
//  Set the initial condition for arm
//
//////////////////////////////////////////////////////////////////////////////////////////////////////
void Rover_Calibration()  {
         
  joint1_on = false;
  joint4_on = false;
  joint5_on = false;
  joint6_on = false;
  joint7_on = false;
  joint2.writeMicroseconds(1500);
  joint3.writeMicroseconds(1500);
  
}

////////////PPM_reader() Taranis Funct //////////////////////////////////////////////////////////////////
//  
//  INPUT - Global arrays for fetching, buffering, retreival(before next iteration)
//  OUTPUT - Global array filled with PPM signals 
//  This code reads 2 sets of values from RC reciever of PPM signals on Pin 2.  It will then store them 
//    in another array to allow the software to continue without interfering with the interrupt calls.
//
//////////////////////////////////////////////////////////////////////////////////////////////////////
void PPM_reader()  {
         
  startTime=micros();           // store time value a when pin value falling
  deltaTime=startTime-endTime;  // calculating time inbetween two peaks
  endTime=startTime;            // delta time of PPM signal
  ppmIN[iterator++]=deltaTime;             // storing 15 value in array
  
  //iterator++;       
  if(iterator==27){
    for(int j=0;j<27;j++){
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
  for(iteration=0; iteration<17; iteration++){
    global_Array[iteration]=buffer_arr[++startPoint];  //assign 6 channel values after separation space
  }
}

//////// Taranis LED testing
/* For debugging if needed
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
*/
/*
  //////// setup LED Testing ///////////////
  for(int x = 3; x < 13; x++)
    pinMode(x, OUTPUT);
  ///////////////////////////////////
*/
