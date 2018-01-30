// This event loop is dependant on a python control script service running of PI
// constants won't change. They're used here to
// set pin numbers:
const int powerPin = 2;     // the number of the power control pin
const int ledPin =  13;      // the number of the LED pin

// variables will control change of state of Raspberry PI:
int resetEvent = 0;      
int shutdownEvent = 0;
int startupEvent = 0;

void setup() {
  // initialize the LED pin as an system monitor:
  pinMode(ledPin, OUTPUT);
  // initialize the OUTPUT to control Reset/OFF/ON state:
  pinMode(powerPin, OUTPUT);
  //Start the Raspberry PI
  digitalWrite(powerPin, HIGH);
}

void loop() {
  if(resetEvent){
    digitalWrite(ledPin, LOW);
    digitalWrite(powerPin, LOW);
    delay(2000);
    digitalWrite(ledPin, HIGH);
    digitalWrite(powerPin, HIGH);
  }
  if(shutdownEvent){
    digitalWrite(ledPin, LOW);
    digitalWrite(powerPin, LOW);
  }
  if(startupEvent){
    digitalWrite(ledPin, HIGH);
    digitalWrite(powerPin, HIGH);
  }
}
