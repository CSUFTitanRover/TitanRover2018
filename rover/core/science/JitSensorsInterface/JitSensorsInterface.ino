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
#include <dht.h>

#include <JitK30.h> //For CO2 K-30 sensor


//For 5TE device, in order to recieve data you must choose a pin that supports interupts
#define DATALINE_PIN_5TE 5
#define INVERTED_5TE 1

//Declare Humidity DHT11 sensor and pin number 7
dht DHT;
#define DHT11_PIN 7

//Temperature sensor
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

//Pressure sensor
MPL3115A2 myPressure;

//SDI Serial communication for 5TE Device for testing soil moisture
SDISerial sdi_serial_connection(DATALINE_PIN_5TE, INVERTED_5TE);

void setup() {
  // put your setup code here, to run once:
  Wire.begin();        // Join i2c bus
  //Serial.begin(9600);  // Start serial for output
  Serial.begin(57600);  // Start serial for output

  
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
  loopSoilSensor_5TE();

  /* Code for DHT11 Humidity Sensor */
  loopHumidity_DHT11();

  /* Code for K-30 CO2 Sensor */
  loopCO2sensor_Jit_K30();
  

  Serial.write("END");
  Serial.write("\n");
  
  delay(2000);
}




//Get Measurement from 5TE Device by sending SDI queries
char* get_measurement(){
  char* service_request = sdi_serial_connection.sdi_query("?M!",1000); //sending our query via connection
  char* service_request_complete = sdi_serial_connection.wait_for_response(1000); //waiting for the response from the sensor
  return sdi_serial_connection.sdi_query("?D0!", 1000); //it'll return as soon as we get a clean response  
}

//Setup code for 5TE
void setup5TE(){
  sdi_serial_connection.begin(); // start our SDI connection
  
  //Serial.println("5TE INITIALIZED"); // startup string echo'd to our uart
  
  //delay(3000); // startup delay to allow sensor to powerup and output its DDI serial string
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

  char* tempPressure = getCharFromLong(pressure);
  Serial.write(tempPressure);  
  Serial.write('\n');
  free(tempPressure);
  

  //float temperature = myPressure.readTemp();
  //Serial.print(" Temp(c):");
  //Serial.print(temperature, 2);
  

  float temperature = myPressure.readTempF();
  //Serial.print(" Temp(f):");
  //Serial.println(temperature,2);

  char* temp = getCharFromFloat(temperature);
   
  Serial.write(temp);
  Serial.write('\n');

  free(temp);
  //Serial.println();
}


char* getCharFromFloat(float num){
  num = num * 100;

  int abc = (int)num;
  char* a = (char*)malloc(256);
  sprintf(a, "%d",abc );
  return a;
}

char* getCharFromInteger(int num){  
  char* a = (char*)malloc(256);
  sprintf(a, "%d",num );
  return a;
}

char* getCharFromLong(float num){
  num = num * 100;

  long abc = (long)num;
  char* a = (char*)malloc(256);
  sprintf(a, "%6ld",abc );
  return a;
}

//Loop code for Melexis MLX90614
void loopTempSensor(){
  
  char* ambTempC = getCharFromFloat(mlx.readAmbientTempC());
  Serial.write(ambTempC); 
  Serial.write('\n');
  free(ambTempC);
  
  char* objTempC = getCharFromFloat(mlx.readObjectTempC());
  Serial.write(objTempC);
  Serial.write('\n');
  free(objTempC);

  
  
  char* ambTempF = getCharFromFloat(mlx.readAmbientTempF()); 
  Serial.write(ambTempF); 
  Serial.write('\n');
  free(ambTempF);

  char* objTempF = getCharFromFloat(mlx.readObjectTempF());
  Serial.write(objTempF);
  Serial.write('\n');
  free(objTempF);  
}


//Loop code for UV Light Sensor
void loopUVLight(){
  int sensor = analogRead(A0);
  float voltage = sensor * 3.3 / 1023;
  float uvindex = voltage / 0.1;
  
  //Serial.print("UV Sensor - ");
  char* tempSensor = getCharFromInteger(sensor);
  Serial.write(tempSensor);
  Serial.write('\n');
  free(tempSensor);

  //Serial.print(" Voltage - ");
  char* tempVolt = getCharFromFloat(voltage);
  Serial.write(tempVolt);  
  Serial.write('\n');
  free(tempVolt);

  //Serial.print(" UV Index - ");  
  char* tempUvIndex = getCharFromFloat(uvindex);
  Serial.write(tempUvIndex);
  Serial.write('\n');
  free(tempUvIndex);
}


//Loop code for Humidity sensor
void loopHumidity_DHT11() {
  
  int chk = DHT.read11(DHT11_PIN);
  
  //Serial.print("Temperature in C = ");
  char* temp = getCharFromFloat(DHT.temperature);
  Serial.write(temp);
  Serial.write('\n');
  free(temp);
  
  //Serial.print("Humidity in % = ");
  char* tempHumidity = getCharFromFloat(DHT.humidity);
  Serial.write(tempHumidity);
  Serial.write('\n');
  free(tempHumidity);
  
  //delay(1000);
}


//Loop code for 5TE Decagon Soil sensor
void loopSoilSensor_5TE() {
  int plusCounter = 0;
    
  char* response = get_measurement();
  
  if (response) {
    char* something = strtok(response, "+");   
    
    while(something != NULL) {
      
      if(plusCounter != 0) {
        Serial.write(something);
        Serial.write('\n');     
      }
      
      something = strtok (NULL, "+"); //Increments to next value after +
      plusCounter++;
    }//While loop ends  
    
  }//If response ends
  
}



//Loop code for K-30 CO2 sensor
void loopCO2sensor_Jit_K30() {
  int co2Value = readCO2();
  
  if (co2Value <= 0) //Means Checksum failed / Communication failure
  {
    co2Value = -1;
  }  

  char* tempCO2 = getCharFromInteger(co2Value);
  Serial.write(tempCO2);
  Serial.write('\n');
  free(tempCO2);
  
  //delay(2000);
}




