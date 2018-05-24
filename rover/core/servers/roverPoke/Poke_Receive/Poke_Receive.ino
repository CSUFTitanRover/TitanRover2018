/* Titan Rover 2018
 *  Maxfield Wilhoite
 *  
 * Poke Receiver Script 
 * Listens for sequence sent by poke.py and executes the finger extension.
 */

#include <SoftwareSerial.h>
char rec = ' ';

SoftwareSerial HC12(3, 2); // HC-12 TX Pin, HC-12 RX Pin

void setup() {
  Serial.begin(9600);             // Serial port to computer
  HC12.begin(9600);               // Serial port to HC12
  pinMode(10,OUTPUT);             // Pin 10, Finger Extender
  pinMode(13,OUTPUT);             // Pin 13, LED
}

void loop() {
  rec = HC12.read();              // Read in byte from receiver
  if (rec == '\n') {              // '\n' first denoting character of sequence sent by poke.py
    String pokeData = "";
    for (int i = 0; i < 4; i++) { // Loop to grab the rest of the sequence sent by poke.py
    delay(50);                    // Delay is needed otherwise the loop goes past the sequence
      rec = HC12.read();
      if (rec == '\n') {          // Check if the initial \n was not sent by poke.py
        i = 0;
        pokeData = "";
      } else {
        pokeData += rec;
      }
    }
    if (pokeData == "poke"){      // Verify that the reading sequence was sent by poke.py
      digitalWrite(10, HIGH);     // Extend finger
      delay(100);
      digitalWrite(10,LOW);       // Retract finger
    }
    else{
      digitalWrite(13, HIGH);     // Blink LED if sequence was incorrect
      delay(100);
      digitalWrite(13, LOW);
    }
  }
}
