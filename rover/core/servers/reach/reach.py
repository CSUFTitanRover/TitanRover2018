import serial
from time import sleep
import re
import sys
import requests
global ser, nvidiaIp
nvidiaIp = "localhost"

while True:
    try:
        ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
        break
    except:
        print("Not Connected to the Reach on /dev/ttyACM0")
        sleep(1)
    
    
pattern = re.compile('(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
print("Waiting for GPS Lock...")
while True:
    data = ser.readline()
    m = re.match(pattern, data)
    if m:
        payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/reach", 
        "data": {"lat": float(m.group(3)), "lon": float(m.group(4)),
        "altitude": float(m.group(5)), "fix": (True if (int(m.group(6)) > 0) else False),
        "nos": int(m.group(7)), "sdn":float(m.group(8)), 
        "sde": float(m.group(9)), "sdu":float(m.group(10)),
        "sdne":float(m.group(11)), "sdeu":float(m.group(12)),
        "sdun":float(m.group(13)), "age":float(m.group(14)), 
        "ratio":float(m.group(15)) }} ]}
        try:
            print("Dumping to deepstream...")
            request = requests.post('http://' + nvidiaIp + ':4080', json=payload)
            print request.text
        except:
            print("Deepstream doesn't seem to be online")
        
        
        sys.stdout.write(m.group(1) + ' ' + m.group(2) + ' ' + m.group(2) + ' '
        + m.group(3) + ' ' + m.group(4) + m.group(5) + ' ' + m.group(6) + ' ' 
        + m.group(7) + ' ' + m.group(8) + ' ' + m.group(9) + ' ' + m.group(10) + ' ' 
        + m.group(11) + ' '+ m.group(12) + ' '+ m.group(13) + ' ' + m.group(14) + ' '
        + m.group(15) + ' '+ '\n')
        
    else:
        print("No valid regex data")
        sleep(1)

    print(data)
