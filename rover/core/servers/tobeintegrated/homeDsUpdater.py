import requests
import json
import subprocess   


def get( recordName):
    if type(recordName) is str:
        payload = {"body":[{"topic": "record", "action":"read", "recordName": "rover/" + recordName}]}
        request = requests.post('http://192.168.1.2:4080', json=payload)
    
    if type(request.content) is bytes:
        response = json.loads(request.content.decode('utf-8'))
    elif type(request.content) is str:
        response = json.loads(request.content)
    
    if response["result"] == "SUCCESS":
        return response["body"][0]["data"]
    elif response["result"] == "FAILURE":
        return "NO_RECORD"
    else:
        return "NO_DEEPSTREAM"


def post( obj, recordName):
    if type(recordName) is str:
        payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/" + recordName, "data": obj}]}
        request = requests.post('http://192.168.1.8:3080', json=payload)


    if type(request.content) is bytes:
        response = json.loads(request.content.decode('utf-8'))
    elif type(request.content) is str:
        response = json.loads(request.content)
    
    if response["result"] == "SUCCESS":
        return response["body"][0]["data"]
    elif response["result"] == "FAILURE":
        return "NO_RECORD"
    else:
        return "NO_DEEPSTREAM"



while True:
    try:
        reach = get('gps')
        imu = get ('imu')
        print("GPS and IMU Data Retrieved from Rover Deepstream")
        post(reach, 'gps')
        post(imu, 'imu')
        print("Gps Data Sent to HomeBase Deepstream")
    except:
        print("Error in forwardnig data")

    
