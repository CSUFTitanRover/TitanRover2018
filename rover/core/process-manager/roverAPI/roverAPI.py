"""
    Richard Stanley
    TitanRover2018
    audstanley@gmail.com
"""

import os
import json
from time import sleep
from subprocess import Popen, PIPE
from flask import Flask, request
"""
Notes:
    localhost:5000/restartScreen/<screenSessionName> 
        # will restart the screen session
        # check ../process.json for the names of the sessions that run on startup

    localhost:5000/clearLogFiles
        # will empty all of the screen log files to save hard drive space

    localhost:5000/log/<screenSessionName>/<numberOfLines>
        # will return the last numberOfLines from the screenNameSession specified
"""




mainDir = os.getcwd()
path = json.load(open('../pathToTitanRover.json'))
processes   = json.load(open('../processes.json'))
app = Flask(__name__)

class c:
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    MAGENTA = '\033[35'
    RED = '\033[31m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if path["path"] is None or path["path"][-1:] == "/":
    print(c.RED+"You need to set the path in the pathToTitanRover.json file"+c.DEFAULT)
    print(c.RED+"    To the path leading up to the /TitanRover2018 file"+c.DEFAULT)
    print(c.RED+"    An example of pathToTitanRover.json might be:"+c.DEFAULT)
    print(c.YELLOW+"      { \"path\": \"/home/pi\" }\n"+c.DEFAULT)
    sys.exit()

splash = "<html><body> Welcome to the Titan Rover API, please view documentation @ \
 <a href='https://github.com/CSUFTitanRover/TitanRover2018/tree/feature/Mobility-Autonomous/rover/core/process-manager'> roverAPI github </a></body></html>"

def clearAllLogs():
    for item in processes:
        fullPath = path["path"] + item["path"] + "screenlog.0"
        try:
            f = open(fullPath, "w")
            f.write("")
            f.close()
            print(c.YELLOW+"Cleared the file: "+c.DEFAULT, fullPath)
        except:
            o = "Didn't clear file: " + fullPath, "\n\t" + fullPath + "may not exist." 
            print(o)

def restartSession(sessionName):
    for item in processes:
        if item["screenName"] == sessionName and sessionName != "roverAPI":
            fullPath = path["path"] + item["path"]
            #os.chdir(fullpath)
            command = '"'+ item["python"] + " "+ item["script"]  +'\\015"' 
            print(command)
            o = Popen(["screen", "-S", item["screenName"], "-X", "kill"], stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8')
            print(o)
            o = Popen(["screen", "-dmLS", item["screenName"]], stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8')
            Popen( ["screen", "-S", sessionName, "-X", "stuff", command ], stdout=PIPE, stderr=PIPE, cwd=fullPath).communicate()
            print(c.YELLOW+"Restarted process:", item["screenName"]+c.DEFAULT)
            print(os.getcwd())
            #os.chdir(mainDir)
            return True
    return False 

def getLogFromSession(screenName, lines):
    for item in processes:
        if item["screenName"] == screenName:
            o = [x for x in processes if x['screenName'] == screenName][0]
            fullPath = str(path["path"]) + str(o["path"])
            p = str(Popen(["cat", "screenlog.0"], cwd=fullPath, stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8'))
            p = p.split("\r\n")
            #print(p)
            p = p[(-1*(1+lines)):]
            return '<br>\n'.join(p).replace("\"", "'").replace("#", "\n")
    return ""
    

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def index():
    return splash

@app.route('/clearLogFiles')
def clearLogFiles():
    try:
        clearAllLogs()
        return '{ "status": "SUCCESS" }'
    except:
        return '{ "status": "FAIL", "reason": "There was a problem clearing all of the log files" }'

@app.route('/restartScreen/<string:sessionName>')
def restartScreen(sessionName):
    print(sessionName)
    if restartSession(sessionName):
        return '{ "status": "SUCCESS" }'
    else:
        return ' { "status": "FAIL", "reason": "No session named: '+sessionName+'"}'

@app.route('/log/<path:filename>')
def getLogs(filename):
    filename = filename.split("/")
    try:
        n = int(filename[1])
    except:
        return '{ "status": "FAIL", "reason": "Format needs to be: /log/screenSessionName/numberOfLines" }'
    s = getLogFromSession(filename[0], n)
    if s != "":
        return '{ "status": "SUCCESS", "data": "'+s+'" }'
    else:
        return('{ "status": "FAIL" }')

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/restartTheRover', methods=['GET'])
def restartTheRover():
    Popen(["init", "6"], stdout=PIPE, stderr=PIPE).communicate()
    return '{ "status": "SUCCESS" }'

@app.route('/shutdownTheRover', methods=['GET'])
def shutdownTheRover():
    print("shutting down the rover..")
    Popen(["init", "0"], stdout=PIPE, stderr=PIPE).communicate()
    return '{ "status": "SUCCESS" }'

@app.route('/syncMotion', methods=['GET'])
def syncMotion():
    try:
        Popen(["rsync", "-prav", "-e", "ssh", "--delete", "/var/lib/motion", "root@192.168.1.3:/home/pi/Images"], stdout=PIPE, stderr=PIPE).communicate()
        o, e = Propen(["ssh", "root@192.168.1.3", "\"chown -R pi:pi /home/pi/images/\""], stdout=PIPE, stderr=PIPE).communicate()
        o = o.decode("utf-8")
        e = e.decode("utf-8")
        print("out:", c.YELLOW, o, c.DEFAULT)
        print("err", c.RED, e, c.DEFAULT)
    if e == "":
        return '{ "status": "SUCCESS" }'
    else:
        return '{ "status": "FAIL" }'

if __name__ == '__main__':
    app.run(debug=True)
