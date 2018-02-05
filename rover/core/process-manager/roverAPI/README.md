# Rover API

> The purpose of the rover API is to easily add functionality to the rover without the use of deepstream.  In some cases, we might need to run a simple command and do not need a database, and this is where the Rover API works well by utilizing Flask we can fire off functions without threading our python scripts.

### Here are the current functions available from the API:
http:127.0.0.1:5000/**functionCalls**/**possibleOtherParameters**

|API|type|purpose| Succssful API return|notes|
| :---- | :---| :---- | :----- | :---- |
|/clearLogFiles| GET | This will clear all screenlog.0 file| { "status": "SUCCESS" }||
|/shutdown|GET|will gracefully shutdown the API. Not to implement in UI, only for testing roverAPI| No JSON returned||
|/restartScreen/\<sessionName\>|GET|Will kill, and completely restart a screen session|{ "status": "SUCCESS" }|Will return { "status":"FAIL" } if the screen session does not exists|
|/log/\<screenName\>/<numberOfLines\> <br>Example:<br>/log/speed/4|GET|This will return the n number of lines from any running screen session| { "status": "SUCCESS", "data": "{'download': 392.0, 'ip': '192.168.1.15', 'upload': 0.0}{'download': 280.0, 'ip': '192.168.1.15', 'upload': 520.0}{'download': 25200.0, 'ip': '192.168.1.15', 'upload': 8970.0}{'download': 20400.0, 'ip': '192.168.1.15', 'upload': 8660.0}"} ||