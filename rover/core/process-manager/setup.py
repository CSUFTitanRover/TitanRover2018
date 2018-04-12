import sys
import os
from shutil import copyfile
from subprocess import Popen, PIPE
import subprocess
import json

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


processes   = json.load(open('processes.json'))
path        = json.load(open('pathToTitanRover.json'))

cronLinesFromProcesses = []

crontab = '/etc/crontab'

if sys.platform != "linux":
        if sys.platform != "linux2":
            print("Your system: " + sys.platform)
            print(c.RED+"\nThis script was written ONLY for Linux OS."+c.DEFAULT)
            sys.exit()

if os.getuid() is not 0:
    print(c.RED+"Please run script as sudo:\n\t"+c.YELLOW+"sudo python setup.py\n"+c.DEFAULT)
    sys.exit()

if path["path"] == None or path["path"][-1:] == "/":
    print(c.RED+"\nYou need to specify a path in the path.json file first.")
    print(" Otherwise, We cannot setup a startup process for you.")
    print(" an EXAMPLE of path.json might look like this:")
    print(c.YELLOW+"    { \"path\": \"/home/audstanley/Documents\" }"+c.DEFAULT)
    print(c.BLUE+"      Your path MUST point to where the TitanRover2018 Folder is.\n\n"+c.DEFAULT)
    print(c.BLUE+"      and you MUST NOT leave a trailing slash in your path\n\n"+c.DEFAULT)
    sys.exit()
else:
    # look to see if screen exists
    p1 = Popen([ "whereis", "screen" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p2 = Popen([ "whereis", "iftop" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p3 = Popen([ "whereis", "pip" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p4 = Popen([ "whereis", "motion" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p5 = Popen([ "whereis", "nmap" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p6 = Popen([ "whereis", "arp-scan" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p7 = Popen([ "whereis", "pip3" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    p8 = Popen([ "whereis", "flask" ], stdout=PIPE, stderr=PIPE).communicate()[0]
    
    # automatically install dependencies if it does not exists.
    if p1[8:] == "":
        print(c.YELLOW+"Installing screen, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "screen", "-y"], stdout=PIPE, stderr=PIPE).communicate()
    
    if p2[7:] == "":
        print(c.YELLOW+"Installing iftop, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "iftop", "-y"], stdout=PIPE, stderr=PIPE).communicate()
    
    if p3[5:] == "":
        print(c.YELLOW+"Installing python-pip, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "python-pip", "-y"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip", "install", "--upgrade", "pip"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip", "install", "simplekml"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip", "install", "pygame"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip", "install", "pyserial"], stdout=PIPE, stderr=PIPE).communicate()

    if p4[8:] == "" or len(p4) == 20:
        print(c.YELLOW+"Installing motion, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "motion", "-y"], stdout=PIPE, stderr=PIPE).communicate()
    
    if p5[6:] == "":
        print(c.YELLOW+"Installing nmap, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "nmap", "-y"], stdout=PIPE, stderr=PIPE).communicate()
    
    if p5[11:] == "":
        print(c.YELLOW+"Installing arp-scan, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "arp-scan", "-y"], stdout=PIPE, stderr=PIPE).communicate()
    
    if p7[6:] == "":
        print(c.YELLOW+"Installing python3-pip, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "python3-pip", "-y"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip3", "install", "--upgrade", "pip"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip3", "install", "simplekml"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip3", "install", "pygame"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip3", "install", "pyserial"], stdout=PIPE, stderr=PIPE).communicate()
    
    if p8[7:] == "":
        Popen([ "sudo", "pip3", "install", "flask"], stdout=PIPE, stderr=PIPE).communicate()

    # Always copy the motion config files (for now), as updates in the future may change
    try:
        copyfile("motionConf/motion.conf", "/etc/motion/motion.conf")
        copyfile("motionConf/thread1.conf", "/etc/motion/thread1.conf")
        copyfile("motionConf/thread2.conf", "/etc/motion/thread2.conf")
        copyfile("motionConf/thread3.conf", "/etc/motion/thread3.conf")
        copyfile("motionConf/thread4.conf", "/etc/motion/thread4.conf")
        print("Created the "+c.YELLOW+"/etc/motion/motion.conf and thread#.conf"+c.DEFAULT+" files")
    except:
        print("There was a problem trying to copy one of the motion configure files")

    try:
        copyfile("udev/99-usb-serial.rules", "/etc/udev/rules.d/99-usb-serial.rules")
        print("Created the "+c.YELLOW+"/etc/udev/rules.d/99-usb-serial.rules"+c.DEFAULT+" file")
    except:
        print("There was a problem trying to copy the udev rules")

    # install python dependencies, if not installed
    try:
        __import__("requests") 
    except:
        print(c.YELLOW+"Installing requests for python, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "python-requests", "-y"], stdout=PIPE, stderr=PIPE).communicate()

    try:
        __import__("simplekml") 
    except:
        print(c.YELLOW+"Installing simplekml for python, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "pip", "install", "simplekml"], stdout=PIPE, stderr=PIPE).communicate()
        Popen([ "sudo", "pip3", "install", "simplekml"], stdout=PIPE, stderr=PIPE).communicate()



    with open(crontab, 'r') as file:
        lines = file.readlines()

    file.close()

    cronLineA   = "@reboot root cd"
    cronLineB   = "&& screen -dmLS"
    cronLineC   = "&& screen -S"
    cronLineD   = "-X stuff \""
    cronLineE   = "\\015\";\n"


    for o in processes:
        # cronLineA           path["path"]                  o["path"]                                             cronLineB                 o["screenName"]      cronLineC       o["screenName"]       cronLineD        o["python"] o["script"]   cronLineD
        # {@reboot root cd} {/home/audstanley/Documents} {/TitanRover2018/rover/core/servers/ArduinoSocketServer/} {&& /usr/bin/screen -dmLS }    {mobility}       {&& screen -S }   {mobility}            { -X stuff "}   {python}     {mobility.py}  \015";\n
        #if os.environ.get("roverType") == "rover":
            #print("OS ENV GOOD")
            #if o["computer"] == os.environ.get("roverType") or o["computer"] == "both":
                #print(o["computer"])
	if(os.path.exists(path["path"] + o["path"] + o["script"])) or o["script"] == "motion":
	    cronLinesFromProcesses.append("{} {}{} {} {} {} {} {}{} {} {}".format(cronLineA, path["path"], o["path"], cronLineB, o["screenName"], cronLineC, o["screenName"], cronLineD , o["python"], o["script"], cronLineE))
                                            #  cA p1p2 cB oS cC oS cD oPoX cE
        else:
            print(c.RED+"Cannot find the roverType variable in /etc/environment:")
            print("    in order to fis this, you need to edit your /etc/environment.")
            print("    on the line under the "+c.BLUE+"PATH="+c.RED+" put:")
            print("    "+c.BLUE+"roverType="+c.DEFAULT+"\"rover\""+c.RED+"# or "+c.DEFAULT+"\"base\""+c.RED)
            print("then the setup will know how to organize your crontab"+c.DEFAULT)
            sys.exit()

        setupCronLine = "0 15 1 * * root cd " + path["path"] + "/TitanRover2018/rover/core/process-manager/ && python getLatestFiles.py;\n"; 
    cronLinesFromProcesses.insert(0, setupCronLine)
    
    #print(cronLinesFromProcesses)
    if len(lines) > 1 and len(cronLinesFromProcesses) > 1:
        dif = [v for v in lines if v not in cronLinesFromProcesses]
        if "roverType" in os.environ:
                if not any("roverType" in s for s in dif):
                    cronLinesFromProcesses.insert(0, "roverType=" + "\"" + os.environ["roverType"] +"\"\n")
        if len(dif) > 0:
            file = open(crontab, 'w')
            for i in dif:
                file.write(i)
            for i in cronLinesFromProcesses:
                file.write(i)
            file.close()

    print(c.BLUE+"\nSetup is now complete\n"+c.DEFAULT)
    print(c.YELLOW+"  Please restart so that default applications may ake effect."+c.DEFAULT)
    print(c.YELLOW+"  If you would like to remove any startup processes:"+c.DEFAULT)
    print(c.YELLOW+"    Edit your /etc/crontab file and remove any process that you may not"+c.DEFAULT)
    print(c.YELLOW+"    want or need."+c.DEFAULT)
    print(c.YELLOW+"  To view your motion cameras navigate to localhost:8081 :8082 :8083 and :8084"+c.DEFAULT)
    print(c.YELLOW+"  To edit the quality of your motion cameras check localhost:8080"+c.DEFAULT)
    print(c.YELLOW+"    Thread 1 -> config -> list -> stream_quality and stream_maxrate "+c.DEFAULT)
    print(c.YELLOW+"      These two options will improve your camera quality with larger numbers"+c.DEFAULT)
    print("\n")
