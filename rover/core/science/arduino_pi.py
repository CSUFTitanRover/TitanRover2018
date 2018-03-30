import serial
import deepstream

NoOfValues = 15 #No of values written by Arduino to Serial
ArduinoPort = '/dev/ttyACM0'

def getArduinoValues():
    printValues = False

    sensorValues = []
    listIndex = 0
    
    ser = serial.Serial(ArduinoPort,57600)
    
    while True:       
        if(ser.inWaiting() > 0):
            readstr = ser.readline()
            readstr = bytes.decode(readstr).rstrip()            

            if("START" in readstr):
                printValues = True
                continue
            elif("END" in readstr and printValues == True):
                return sensorValues
                

            if(printValues):
                sensorValues.append(readstr)
                #print(readstr)  #Print each value coming from sensor



def ListToDict(values):
    dictValues = {}

    dictValues['MPL3115A2_Pressure(Pa)']=   float(values[0]) / 100
    dictValues['MPL3115A2_Temp_inF']    =   float(values[1]) / 100
    dictValues['UV_SensorValue']        =   int(values[2])
    dictValues['UV_SensorVoltage']      =   float(values[3]) / 100
    dictValues['UV_Index']              =   float(values[4]) / 100
    dictValues['Ambient_Temp_inC']      =   float(values[5]) / 100
    dictValues['Object_Temp_inC']       =   float(values[6]) / 100
    dictValues['Ambient_Temp_inF']      =   float(values[7]) / 100
    dictValues['Object_Temp_inF']       =   float(values[8]) / 100    
    dictValues['Electrical_Conductivity']   = values[9]
    dictValues['Volumetric_Water_Content']  = values[10]
    dictValues['5TE_Temperature']           = values[11]
    dictValues['DHT11_TemperatureInC']      = float(values[12]) / 100
    dictValues['DHT11_HumidityInPerc']      = float(values[13]) / 100
    dictValues['K30_CO2_ValueInPPM']        = int(values[14])
    
    return dictValues



proceed=True

while(proceed):    
    response = input("Do you want to fetch values (y/n) -")
    if(response == 'y'):
        listLength = 0

        values = []
        
        while(listLength != NoOfValues):            
            values = getArduinoValues()
            listLength = len(values)
            #print(listLength) #Prints the length of the sensor values list

        DictSensorValues = ListToDict(values)
        print(DictSensorValues)

        saveValues =  input("Do you want to save sensor values (y/n) -")

        if(saveValues == "y"):
            try:
                mesg = deepstream.post(DictSensorValues, "Jit_ScienceSensorData")
                if(mesg.upper() == "SUCCESS"):
                    print("Sensor values posted to Deepstream record Jit_ScienceSensorData")           
            except:
                print("An error occured while posting to Deepstream")
        
    else:
        proceed = False


