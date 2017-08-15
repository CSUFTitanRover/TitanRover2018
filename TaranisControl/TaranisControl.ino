unsigned long int startTime,endTime,deltaTime;
volatile int ppmIN[18],buffer_arr[18],iterator ,global_Array[8];
//specifing arrays and variables to store values 

void setup() {
  Serial.begin(9600);
  // enabling interrupt at pin 2
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), read_me, RISING);
  //initialize the counter
  iterator = 0;
}

void loop() {
  read_Array();
  //For debugging if needed
  /*for(int b = 0; b < 8; b++){
    Serial.print(global_Array[[b]);
    Serial.print("\t");
  }
  Serial.print("\n");
  delay(100);*/

  
}
////////////read_me()/////////////////////////////////////////////////////////////////////////////////
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

////////////read_Array()/////////////////////////////////////////////////////////////////////////////////
//  
//  INPUT - Global array of next iteration
//  OUTPUT - Global array filled with PPM signals 
//  
//
//////////////////////////////////////////////////////////////////////////////////////////////////////
void read_Array(){
  int iteration, startPoint, ppmGap = 0;
  for( ppmGap = 9; ppmGap > -1; ppmGap-- )
    if(buffer_arr[startPoint]>5000){
      startPoint = ppmGap;  //detecting separation space 10000us in that another array                     
      break;
    }
  for(iteration=0; iteration<8; iteration++){
    global_Array[iteration]=buffer_arr[++startPoint];  //assign 6 channel values after separation space
  }
}
