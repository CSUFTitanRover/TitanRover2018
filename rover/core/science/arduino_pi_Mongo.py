import datetime
import serial
from pymongo import MongoClient    

NoOfValues = 14 #No of values written by Arduino to Serial
ArduinoPort = '/dev/ttyACM0'
BaudRate = 57600

MongoServer = '127.0.0.1'
MongoPort = 27017

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



# Returns a MongoDB collection
def connectMongo():
    try:
    
        client = MongoClient(MongoServer, MongoPort)
        db = client.titanrover

        scienceCollection = db.science

        return scienceCollection

    except:
        print('Error in connecting to MongoDB')
        return None


def ListToDict(values):
    dictValues = {}

    dictValues['Timestamp']             =   datetime.datetime.now()
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
    
    return dictValues


# Save to MongoDB
def SaveData(collection, dictData):

    try:

        # For PyMongo version 3.*
        # objectId = collection.insert_one(dictData).inserted_id

        # For PyMongo version 2.7.*
        objectId = collection.insert(dictData)
        
        
        print('\nData saved to MongoDB with ObjectId {0}\n'.format(objectId))

    except:
        print('Error occured in MongoDB insert')        
        
    




science = connectMongo()

proceed=True

while(proceed):    
    listLength = 0

    values = []
    
    while(listLength != NoOfValues):            
        values = getArduinoValues()
        listLength = len(values)
        

    DictSensorValues = ListToDict(values)
    
    
    print(DictSensorValues)       
    
    SaveData(science, DictSensorValues)        
