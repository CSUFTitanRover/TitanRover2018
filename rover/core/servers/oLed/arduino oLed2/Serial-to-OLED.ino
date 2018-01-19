#include <SoftwareSerial.h>
#include "U8glib.h"

SoftwareSerial rxData(10, NOT_A_PIN);
U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NO_ACK);
//U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_DEV_0|U8G_I2C_OPT_NO_ACK|U8G_I2C_OPT_FAST);	// Fast I2C / TWI 

const char* skull = "x";
const char* solidCircle = "F";
const char* starShipEnterprise = "®";

const int rightLineLength = 7;

char c;

// convert String to char array
// Don't forget char \0
// Left side of OLED screen
char dataHold[20] = ".................\0";
char line0[rightLineLength] = ".....\0";
char line1[rightLineLength] = ".....\0";
char line2[rightLineLength] = ".....\0";
char line3[rightLineLength] = ".....\0";
char line4[rightLineLength] = ".....\0";
char line5[rightLineLength] = ".....\0";

// Right Side of OLED screen
char line6[14] = "............\0";


unsigned int delem = 0;
unsigned int l0Count = 0;
//unsigned int l1Count = 0;
//unsigned int l2Count = 0;
//unsigned int l3Count = 0;
//unsigned int l4Count = 0;
//unsigned int l5Count = 0;

const int r1 = 15;
const int r2 = 24;
const int r3 = 33;
const int r4 = 42;
const int r5 = 51;
const int r6 = 60;

const int c1 = 1;
const int c2 = 38;
const int c3 = 67;
const int c4 = 96;


int availableBytes;



// THIS IS THE LOOP THAT RUNS FOREVER
void draw(void) {
  // graphic commands to redraw the complete screen should be placed here 

  


  u8g.setFont(u8g_font_4x6);
  //u8g.setFont(u8g_font_osb21);
  // numbers for u8g.drawStr(rightPixels, downPixels)
  
  // go down every 10 pixels for the List
  u8g.drawStr( 30, 6, "Titan Rover Sys");
  u8g.drawLine(1, 8, 124, 8);
  u8g.drawLine(65, 8, 65, 60);



  u8g.drawStr( c1, r1, "Heading:");
  u8g.drawStr( c2, r1, line0);

  u8g.drawStr( c1, r2, "Pitch:");
  u8g.drawStr( c2, r2, line1);

  u8g.drawStr( c1, r3, "Roll:");
  u8g.drawStr( c2, r3, line2);
  
  u8g.drawStr( c1, r4, "MagCal:");
  u8g.drawStr( c2, r4, line3);

  u8g.drawStr( c1, r5, "downLD:");
  u8g.drawStr( c2, r5, line4);
  
  u8g.drawStr( c1, r6, "upLD:");
  u8g.drawStr( c2, r6, line5);


  //u8g.drawStr( 67, 24, "upLD:");
  //u8g.drawStr( 95, 24, line5);

  //u8g.drawStr( 66, 15, "ip:");
  u8g.drawStr( 72, 15, line6);
  
  //Symbols of online or offline:
  u8g.setFont(u8g_font_cursor);
  // 'x' is the symbol for a skull
  //u8g.drawStr( 56, 14, skull);
  // 'F' is a solid circle
  //u8g.drawStr( 56, 24, solidCircle);
  //u8g.drawStr( 56, 32, starShipEnterprise);
  //u8g.setFont(u8g_font_4x6);

  //rxData.flush();

}


void setup(void) {
  //SoftwareSerial setup
  rxData.begin(9600);
  
  // setup LED for blink on reading rxData
  pinMode(LED_BUILTIN, OUTPUT);

  // for a loopback test
  // Serial.begin(9600);
  // while (!Serial) {
  //  ; // wait for serial port to connect. Needed for native USB port only
  // }

  //if(rxData.available()) {
  //    serialData = rxData.read();
  //}

  // flip screen, if required
  // u8g.setRot180();
  
  // set SPI backup if required
  //u8g.setHardwareBackup(u8g_backup_avr_spi);

  // assign default color value
  if ( u8g.getMode() == U8G_MODE_R3G3B2 ) {
    u8g.setColorIndex(255);     // white
  }
  else if ( u8g.getMode() == U8G_MODE_GRAY2BIT ) {
    u8g.setColorIndex(3);         // max intensity
  }
  else if ( u8g.getMode() == U8G_MODE_BW ) {
    u8g.setColorIndex(1);         // pixel on
  }
  else if ( u8g.getMode() == U8G_MODE_HICOLOR ) {
    u8g.setHiColorByRGB(255,255,255);
  }
  
  //pinMode(8, OUTPUT);
}

void loop(void) {
  

  // picture loop
  u8g.firstPage();  
  do {
    
    
    
    availableBytes = rxData.available();
    if(availableBytes) {
      for(int j=0;j<availableBytes;++j) {
          c = rxData.read();
          dataHold[j] = c;
      } 
      delay(1);
    }
    for(int i=0;i<6;++i)           line0[i] = dataHold[i];
    for(int i=6,j=0;i<12;++i,++j)  line1[j] = dataHold[i];
    for(int i=12,j=0;i<18;++i,++j) line2[j] = dataHold[i];
    for(int i=18,j=0;i<24;++i,++j) line3[j] = dataHold[i];
    for(int i=24,j=0;i<30;++i,++j) line4[j] = dataHold[i];
    for(int i=30,j=0;i<36;++i,++j) line5[j] = dataHold[i];

    for(int i=36,j=0;i<50;++i,++j) line6[j] = dataHold[i];
    delay(10);
    rxData.flush();
    //rxData.flush();
    //if(dataHold != "") {
    //  for(int i=0;i<5; ++i)  line0[i] = dataHold[i];
      //for(int i=5;i<11; ++i)  line1[i] = dataHold[i];
    //}
    
      
    //availableBytes = 0;
    

    //Serial.write(line0);
    draw();
  } while( u8g.nextPage() );
  
  // rebuild the picture after some delay
  //delay(2);
}
