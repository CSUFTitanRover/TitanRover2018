/*
 Combined code for all sensors
 By: Jithin J Eapen 
 Date: January 15th, 2018
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).

 Sensors-
 MPL3115A2 library to display the current altitude and temperature
 GUVA-S12SD reading values from Analog Input pin A0 for UV Light Sensing
 5TE Sensor (Decagon Devices)read values from Digital Interrupt Pin 5 using SDI to serial communication
 
 Hardware Connections (Breakoutboard to Arduino):
 -VCC = 3.3V
 
 */


#include <Wire.h>

#include "SparkFunMPL3115A2.h"
#include <Adafruit_MLX90614.h>
#include <SDISerial.h>

//For 5TE device, in order to recieve data you must choose a pin that supports interupts
#define DATALINE_PIN_5TE 5
#define INVERTED_5TE 1

//Temperature sensor
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

//Pressure sensor
MPL3115A2 myPressure;

//SDI Serial communication for 5TE Device for testing soil moisture
SDISerial sdi_serial_connection(DATALINE_PIN_5TE, INVERTED_5TE);

void setup() {
  // put your setup code here, to run once:
  Wire.begin();        // Join i2c bus
  Serial.begin(9600);  // Start serial for output

  
  myPressure.begin(); // Get sensor online

  // Configure the sensor
  //myPressure.setModeAltimeter(); // Measure altitude above sea level in meters
  myPressure.setModeBarometer(); // Measure pressure in Pascals from 20 to 110 kPa  
  myPressure.setOversampleRate(7); // Set Oversample to the recommended 128
  myPressure.enableEventFlags(); // Enable all three pressure and temp event flags

  
  
  //Serial.write("Adafruit MLX90614 test");
  mlx.begin();

  
  //Setup 5TE
  setup5TE();
}

void loop() {

  Serial.write("START");
  Serial.write("\n");
  
  /* Code for Pressure/Altitude sensor MPL3115A2 */  
  loopPressure();

  /* Code for UV Light sensor GUVA-S12SD */
  loopUVLight();  

  /* Code for Temperature sensor Melexis MLX90614 */
  loopTempSensor();

  /* Code for 5TE Sensor */
  loop5TE();

  

  Serial.write("END");
  Serial.write("\n");
  
  delay(500);
}




//Get Measurement from 5TE Device by sending SDI queries
char* get_measurement(){
  char* service_request = sdi_serial_connection.sdi_query("?M!",150);
  //you can use the time returned above to wait for the service_request_complete
  char* service_request_complete = sdi_serial_connection.wait_for_response(150);
  //dont worry about waiting too long it will return once it gets a response
  return sdi_serial_connection.sdi_query("?D0!",150);
}

//Setup code for 5TE
void setup5TE(){
  sdi_serial_connection.begin(); // start our SDI connection
  
  //Serial.println("5TE INITIALIZED"); // startup string echo'd to our uart
  
  delay(3000); // startup delay to allow sensor to powerup and output its DDI serial string
}

//Loop code for Pressure sensor
void loopPressure() {
  /*  float altitude = myPressure.readAltitude();
  Serial.print("Altitude(m):");
  Serial.print(altitude, 2);

  altitude = myPressure.readAltitudeFt();
  Serial.print(" Altitude(ft):");
  Serial.print(altitude, 2);*/

  float pressure = myPressure.readPressure();
  //Serial.println("MPL3115A2 Pressure(Pa):");
  //Serial.println(pressure, 2);
  Serial.write(getCharFromLong(pressure));  
  Serial.write('\n');
  

  //float temperature = myPressure.readTemp();
  //Serial.print(" Temp(c):");
  //Serial.print(temperature, 2);
  

  float temperature = myPressure.readTempF();
  //Serial.print(" Temp(f):");
  //Serial.println(temperature,2); 
  Serial.write(getCharFromFloat(temperature));  
  Serial.write('\n');
  //Serial.println();
}

char* getCharFromFloat(float num){
  num = num * 100;

  int abc = (int)num;
  char a[256];
  sprintf(a, "%d",abc );
  return a;
}

char* getCharFromInteger(int num){  
  char a[256];
  sprintf(a, "%d",num );
  return a;
}

char* getCharFromLong(float num){
  num = num * 100;

  long abc = (long)num;
  char a[256];
  sprintf(a, "%6ld",abc );
  return a;
}

//Loop code for Melexis MLX90614
void loopTempSensor(){
  
  //Serial.print("Ambient = "); 
  //Serial.println(mlx.readAmbientTempC()); 
  Serial.write(getCharFromFloat(mlx.readAmbientTempC())); 
  Serial.write('\n');
  //Serial.print("*C\tObject = "); 
  //Serial.println(mlx.readObjectTempC()); //Serial.println("*C");
  Serial.write(getCharFromFloat(mlx.readObjectTempC()));
  Serial.write('\n');

  
  
  //Serial.print("Ambient = ");
  
  //Serial.println(mlx.readAmbientTempF());
  
  
  
   
  Serial.write(getCharFromFloat(mlx.readAmbientTempF())); 
  Serial.write('\n');
  
  Serial.write(getCharFromFloat(mlx.readObjectTempF())); //Serial.println("*F");
  Serial.write('\n');

  //Serial.println();
}


//Loop code for UV Light Sensor
void loopUVLight(){
  int sensor = analogRead(A0);
  float voltage = sensor * 3.3 / 1023;
  float uvindex = voltage / 0.1;
  
  //Serial.print("UV Sensor - ");
  Serial.write(getCharFromInteger(sensor));
  Serial.write('\n');

  //Serial.print(" Voltage - ");
  Serial.write(getCharFromFloat(voltage));
  Serial.write('\n');

  //Serial.print(" UV Index - ");
  //Serial.write(getCharFromFloat(uvindex));
  Serial.write(getCharFromFloat(uvindex));
  Serial.write('\n');
  //Serial.println();
}




//Loop code for 5TE
void loop5TE(){
  
  //Variable declarations
  String VWC;   //volumetric water content
  String EC;    // electrical conductivity
  String TEMP;  // temperature
  char *FTEvalue=new char[20];

  
  char* response = get_measurement(); // get measurement data
  String FTE=response;
  char tmp1='+';  
  int tmp2=FTE.indexOf(tmp1);
   
  while(tmp2!=1)
  {
    char* response = get_measurement(); // get measurement data
    FTE=response;
    tmp2=FTE.indexOf(tmp1);
  }
   
  int FTElength=FTE.length();
  
  FTE.toCharArray(FTEvalue,FTElength);
  int plustest=FTEvalue[5];
  if (plustest=43)
    {          
      VWC= String(FTEvalue[2])+String(FTEvalue[3])+String(FTEvalue[4]);
      EC= String(FTEvalue[6])+String(FTEvalue[7])+String(FTEvalue[8])+String(FTEvalue[9]);
      TEMP= String(FTEvalue[11])+String(FTEvalue[12])+String(FTEvalue[13])+String(FTEvalue[14]);
    }
    else
    {
      VWC= String(FTEvalue[2])+String(FTEvalue[3])+String(FTEvalue[4])+String(FTEvalue[5]);
      EC= String(FTEvalue[7])+String(FTEvalue[8])+String(FTEvalue[9])+String(FTEvalue[10]);
      TEMP= String(FTEvalue[12])+String(FTEvalue[13])+String(FTEvalue[14])+String(FTEvalue[15]);
    }
  float VWCvalue=VWC.toInt()/100;

  char ECchar[10];
  EC.toCharArray(ECchar,10);

  char TEMPchar[10];
  TEMP.toCharArray(TEMPchar,10);
  
  //Serial.println("VWCvalue      EC       TEMP");  
  Serial.write(getCharFromFloat(VWCvalue));  
  Serial.write('\n');
  //Serial.print("         ");
  Serial.write(ECchar);  
  Serial.write('\n');
  //Serial.print("       ");
  Serial.write(TEMPchar);  
  Serial.write('\n');
  //delay(2000);
}
