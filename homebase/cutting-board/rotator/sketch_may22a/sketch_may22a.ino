int pinDirection = 5; 
int pinPulse = 7;
int pinEnable = 9;
int pinAnalog = A0;
int x = 0;
void setup() {
  Serial.begin(9600);
  pinMode(pinAnalog, INPUT);
  pinMode(pinDirection, OUTPUT);
  pinMode(pinPulse, OUTPUT);
  pinMode(pinEnable, OUTPUT);
  // put your setup code here, to run once:

}

void loop() {
  if(analogRead(pinAnalog) < 768 && analogRead(pinAnalog) > 256)
  {
  // put your main code here, to run repeatedly:
  //delay(10000000000000000);
  for(;x < 45/((1.8)/51);x++)
  {
    digitalWrite(pinEnable, LOW);
    digitalWrite(pinDirection, HIGH);
    digitalWrite(pinPulse, HIGH);
    delayMicroseconds(500);
    digitalWrite(pinPulse, LOW);
    delayMicroseconds(500);
    Serial.println(analogRead(pinAnalog));
  }
  delay(1000);
  Serial.println(analogRead(pinAnalog));
/*if(analogRead(pinAnalog) > 514)
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
 }*/
  }
}
