import json
import requests
from time import sleep

######  global variables for counter, slp(sleepTime), angle1, and angle2  ######

global i
i = 0
global slp
slp = 0.1
global ang1
ang1 = 0
global ang2
ang2 = 0


######  This function calulates the angular velocity in deg/sec  ######

def angularVelocity(ang1, ang2):
    if ang1 > ang2:
        velocity = (ang1 - ang2) / slp
    else:
        velocity = (ang2 - ang1) / slp

    return velocity

######  This functions gets data every slp seconds from deepstream  ######

while True:
    try:
        payload = {"body" : [{"topic" : "record", "action" : "read", "recordName" : "rover/imu"}]}
        request = requests.post('http://127.0.0.1:4080', json=payload)

        if type(request.content) is bytes:
            response = json.loads(request.content.decode('utf-8'))
        elif type(request.content) is str:
            response = json.loads(request.content)

        if response["result"] is "SUCCESS":
            ang1 = response["body"][0]["data"]["heading"]
        elif response["result"] is "FAILURE":
            print("NO RECORD FOUND")
   
        if i > 0 and ang1 != ang2:
            velocity = angularVelocity(ang1, ang2)
        else:
            velocity = 0

        print("Heading:", ang1, "Angular velocity:", velocity)
        sleep(slp)
        ang2 = ang1
        i += 1

    except:
       print("Can't load Deepstream")
