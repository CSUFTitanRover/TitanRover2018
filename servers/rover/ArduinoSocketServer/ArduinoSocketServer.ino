//Sabertooth Communications
#include <SoftwareSerial.h>
#include "Sabertooth.h"

#include <SPI.h>         // needed for Arduino versions later than 0018
//Network setup
#include <Ethernet2.h>
#include <EthernetUdp2.h>

SoftwareSerial SWSerial(NOT_A_PIN, 1);
Sabertooth ST(128, SWSerial);

int packetSize;
// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0x90, 0xA2, 0xDA, 0x10, 0x30, 0xD3
};
byte ip[] = {192, 168, 1, 177};
byte gateway[] = {192,168,1,1};
byte subnet[] = {255,255,255,0};

unsigned int localPort = 5000;      // local port to listen on

char charToIntArray[10];
int moveMentArray[10];

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //buffer to hold incoming packet,
//char  ReplyBuffer[] = "acknowledged";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

//String datReg;

void setup() {
  // put your setup code here, to run once:
  SWSerial.begin(9600);
  ST.autobaud();
  //create an initalization function
  ST.motor(1, 0);
  ST.motor(2, 0);
  //Serial.begin(9600);  
  // start the Ethernet and UDP:
  Ethernet.begin(mac, ip, gateway, subnet);
  Udp.begin(localPort);

  delay(1500); //give a sec to start process
}
// This loop will be a command loop for each of the arduino processes
void loop() {
  packetSize = Udp.parsePacket();
  //Serial.println(Udp.remoteIP());
  //Serial.println(Udp.remotePort());
  
  
  
  Udp.write(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
  if (packetSize) {
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    
    for(int x,y,n = 0; x < packetSize; x++, y++){
      charToIntArray[y] = packetBuffer[x];
      
      if(charToIntArray[y] == ','){
        charToIntArray[y] = '\0';
        moveMentArray[n++] = atoi(charToIntArray);
        y = -1;
        memset(charToIntArray,0,sizeof(charToIntArray));
      }else if(x + 1 == packetSize){
        charToIntArray[++y] = '\0';
        moveMentArray[n++] = atoi(charToIntArray);
        y = -1;
        memset(charToIntArray,0,sizeof(charToIntArray));
      }
      
    }
  
      
    //String datReg(packetBuffer);
    //Need to get JSON working for this transfer of commands and remove switch
    for(int x = 0; x < 10; x++){
      switch (x){
        case 0: 
        {
          ST.drive(moveMentArray[0]);
          //Serial.println(moveMentArray[0]);
          break;
        }
        case 1:{
          ST.turn(moveMentArray[1]);
          //Serial.println(moveMentArray[1]);
          break;  
        }
          //whatever
      }  
    }
  
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write("ready");
  Udp.endPacket();
   
  }         
  memset(packetBuffer,0,sizeof(UDP_TX_PACKET_MAX_SIZE));
}
