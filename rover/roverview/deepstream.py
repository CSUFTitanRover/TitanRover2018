'''
    Richard Stanley
    TitanRover 2017
    audstanley@gmail.com
'''
import requests
import json
import subprocess
from subprocess import Popen


roverIp = "192.168.1.2"   # This ip will change periodically, 
                        # for now, this is the ip of the rover on openvpn

'''
try:
    if "titan" == Popen(["iwgetid", "-r"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]:
        roverIp = "192.168.1.2"
        #print('Your Deepstream IP address is : ' + str(roverIp))
    elif "00:24:B2:CA:8B:86" in Popen(["nmap", "-sP", "192.168.1.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]:
        roverIp = "192.168.1.2"
        #print('Your Deepstream IP address is : ' + str(roverIp))
    else:
        roverIp = "127.0.0.1"
        #print('Your Deepstream IP address is : ' + str(roverIp))
except:
    roverIp = "127.0.0.1"
'''
def get(recordName):
    '''
        The get function will get the entire record "rover/" + recordName
        and returns the record as an object.

        Possible return Errors:
            If the record does not exists in DeepStream, returns "NO_RECORD"
            Else there is no connection to DeepStream,   returns "NO_DEEPSTREAM"

    '''
    response = None
    if type(recordName) is not str:
        raise "Your argument needs to be a string when getting from deepstream"
    payload = {"body":[{"topic": "record", "action":"read", "recordName": "rover/" + recordName}]}
    request = requests.post('http://' + roverIp + ':4080', json=payload)
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


def post(obj, recordName):
    '''
        This function will post the object sen to the deepstream server.

        Arguments:
            obj: an object that you want to post to deepstream
            recordName: the name of the record that you want to post to
    '''
    if type(recordName) is not str:
        raise "Your second argument needs to be a string when setting data to deepstream"
    if type(obj) is not dict:
        raise "Your first argument needs to be a dict setting data to deepstream"
    payload = {"body":[{"topic": "record", "action":"write", "recordName": "rover/" + recordName, "data": obj}]}
    request = requests.post('http://' + roverIp + ':4080', json=payload)
    if request is not None:
        if type(request) is bytes:
            request = request.decode('utf-8')    
        response = request.json()
        return response["result"]
    else:
        return "NO_DEEPSTREAM"
