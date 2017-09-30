//Sabertooth Communications
#include <SoftwareSerial.h>
#include "Sabertooth.h"

#include <SPI.h>         // needed for Arduino versions later than 0018
//Network setup
#include <Ethernet2.h>
#include <EthernetUdp2.h>

SoftwareSerial SWSerial(NOT_A_PIN, 1);
Sabertooth ST(128, SWSerial);


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0x90, 0xA2, 0xDA, 0x10, 0x30, 0xD3
};
byte ip[] = {192, 168, 1, 177};
byte gateway[] = {192,168,1,1};
byte subnet[] = {255,255,255,0};

unsigned int localPort = 5000;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //buffer to hold incoming packet,
char  ReplyBuffer[] = "acknowledged";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

//String datReg;

void setup() {
  // put your setup code here, to run once:
  SWSerial.begin(9600);
  ST.autobaud();
  
  // start the Ethernet and UDP:
  Ethernet.begin(mac, ip, gateway, subnet);
  Udp.begin(localPort);

  delay(1500); //give a sec to start process
}
// This loop will be a command loop for each of the arduino processes
void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    String datReg(packetBuffer);
    //Need to get JSON working for this transfer of commands and remove switch
    switch (str2int(datReg))
    {
      case "run": 
      {
        for(int power = 0; power < 127; power++){
          ST.motor(1,power);
          ST.motor(2,power);
          delay(20);
        }
        for(int power = 127; power > -127; power--){
          ST.motor(1,power);
          ST.motor(2,power);
          delay(20);
        }
        for(int power = -127; power < 0; power++){
          ST.motor(1,power);
          ST.motor(2,power);
          delay(20);
        }
        break;
      }
      case "stop":{
        ST.motor(1,0);
        ST.motor(2,0);
        break;  
      }
      case "arm":{

        //whatever
      }
    }
  }         
}
