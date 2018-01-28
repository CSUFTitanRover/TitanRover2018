//David Feinzimer
//dfeinzimer@gmail.com
//Jan 19 2018

int potPin = 0;
int val = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  val = analogRead(potPin);    // read the value from the sensor
  Serial.println(val);
}
