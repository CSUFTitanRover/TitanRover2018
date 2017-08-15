unsigned long int a,b,c;
volatile int x[18],chl[18],i,ch[8];
//specifing arrays and variables to store values 

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), read_me, RISING);
  // enabling interrupt at pin 2
  i = 0;
}

void loop() {
  read_rc();
  
  for(int b = 0; b < 8; b++){
    Serial.print(ch[b]);
    Serial.print("\t");
  }
  Serial.print("\n");
  delay(100);
}


void read_me()  {
         //this code reads value from RC reciever from PPM pin (Pin 2 or 3)
         //this code gives channel values from 0-1000 values 
         //    -: ABHILASH :-    //
  a=micros(); //store time value a when pin value falling
  c=a-b;      //calculating time inbetween two peaks
  b=a;        // 
  x[i]=c;     //storing 15 value in array
  i=i+1;       
  if(i==18){
    for(int j=0;j<18;j++){
      chl[j]=x[j];
    }
    i=0;
  }
}//copy store all values from temporary array another array after 15 reading  

void read_rc(){
  int i,j,k=0;
  for( k=9; k>-1; k--)
    if(chl[k]>5000){
      j=k;  //detecting separation space 10000us in that another array                     
      break;
    }
  for(i=0;i<8;i++){
    ch[i]=chl[++j];  //assign 6 channel values after separation space
  }
}
