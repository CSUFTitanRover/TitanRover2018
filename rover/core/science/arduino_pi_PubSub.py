import serial
import deepstreamPubSub

NoOfValues = 16 #No of values written by Arduino to Serial
ArduinoPort = '/dev/ttyACM0'
BaudRate = 57600

def getArduinoValues():
    printValues = False

    sensorValues = []
    listIndex = 0
    
    ser = serial.Serial(ArduinoPort,BaudRate)
    
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
    dictValues['Anemometer_WindSpeed']        = int(values[15]) / 100
    
    return dictValues



def PublishEvent(dictData, event, dictName):
    try:
        if(dictName == ''):
            mesg = deepstreamPubSub.publish(event, dictData)
        else:
            mesg = deepstreamPubSub.publish(event, dictData[dictName])
        
        if(mesg.upper() == "SUCCESS"):
            print("Event {0} published to Deepstream".format(event))
    except:
        print("An error occured while publishing {0} to Deepstream".format(event))




def SaveData(dictData):
    
    # Publish all data
    PublishEvent(dictData,"sensors/All",'')        
        
    # Publish individual sensor data
    PublishEvent(dictData,"sensors/MPL3115A2",'MPL3115A2_Pressure(Pa)')
    PublishEvent(dictData,"sensors/GUVAS12SD",'UV_Index')
    PublishEvent(dictData,"sensors/MLX90614_Ambient",'Ambient_Temp_inC')
    PublishEvent(dictData,"sensors/MLX90614_Object",'Object_Temp_inC')
    PublishEvent(dictData,"sensors/Decagon5TE_EC",'Electrical_Conductivity')
    PublishEvent(dictData,"sensors/Decagon5TE_VWC",'Volumetric_Water_Content')
    PublishEvent(dictData,"sensors/DHT11",'DHT11_HumidityInPerc')
    PublishEvent(dictData,"sensors/K30",'K30_CO2_ValueInPPM')
    PublishEvent(dictData,"sensors/Anemometer",'Anemometer_WindSpeed')
    




proceed=True

while(proceed):    
    listLength = 0

    values = []
    
    while(listLength != NoOfValues):            
        values = getArduinoValues()
        listLength = len(values)
        

    DictSensorValues = ListToDict(values)
    
    
    print(DictSensorValues)       
    
    SaveData(DictSensorValues)        
