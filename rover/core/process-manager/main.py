from os import system
import os
import json
from subprocess import Popen
import subprocess
from deepstream import get, post
import sys
from time import sleep
import curses
from threading import Thread
global keyIn, screen, iftop, reach, imu
iftop       = {}
iftopTail   = ""
reach       = {}
reachTail   = ""
imu         = {}
imuTail     = ""
keyIn       = 0

path        = json.load(open('pathToTitanRover.json'))
processes   = json.load(open('processes.json'))

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

if os.getuid() is not 0:
    print(c.RED+"Please run script as sudo:\n\t"+c.YELLOW+"sudo python main.py\n"+c.DEFAULT)
    sys.exit()

if sys.platform != "linux":
        if sys.platform != "linux2":
            print("Your system: " + sys.platform)
            print(c.RED+"\nThis script was written ONLY for Linux OS."+c.DEFAULT)
            sys.exit()

path = json.load(open('pathToTitanRover.json'))
if path["path"] is None or path["path"][-1:] == "/":
    print(c.RED+"You need to set the path in the pathToTitanRover.json file"+c.DEFAULT)
    print(c.RED+"    To the path leading up to the /TitanRover2018 file"+c.DEFAULT)
    print(c.RED+"    An example of pathToTitanRover.json might be:"+c.DEFAULT)
    print(c.YELLOW+"      { \"path\": \"/home/pi\" }\n"+c.DEFAULT)
    sys.exit()

def cleanUpScreenLogs():
    for item in processes:
        fullPath = path["path"] + item["path"] + "screenlog.0"
        f = open(fullPath, "w")
        f.write("")
        f.close()

cleanUpScreenLogs()

screen = curses.initscr()
curses.noecho()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def restartProcess(screenName):
    o = [x for x in processes if x['screenName'] == screenName][0]
    sn = str(o["screenName"])
    fullPath = str(path["path"]) + str(o["path"])
    py = str(o["python"])
    scrpt = str(o["script"]) + "\015\""
    cmd = py + " " + scrpt
    p = Popen([ "screen", "-S", screenName, "-X", "kill"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    p = Popen(["screen", "-dmLS", sn], cwd=fullPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    p = Popen(["screen", "-S", sn, "-X", "stuff", cmd], cwd=fullPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def runWindow():
    global keyIn, screen, iftop, imu, reach
    
    while keyIn != ord(chr(27)):
        screen = curses.initscr()
        screen.clear()
        screen.border(0)

        screen.addstr(1, 2, "Titan Rover CLI Process Manager", curses.color_pair(1))
        screen.addstr(2, 4, "To restart a process, type the number of the listed process", curses.color_pair(3))
        screen.addstr(3, 4, "To exit, hold the ESC key", curses.color_pair(3))
        screen.addstr(4, 4, "Process List:")
        screen.addstr(6, 6,  "    imu:")
        screen.addstr(12, 6,  "    reach:")
        screen.addstr(18, 6, "1 - iftop: ")

        
        if type(imu) == dict:
            if imu == {}:
                screen.addstr(6, 25, "WAITING ON IMU...", curses.color_pair(2))
            else:
                screen.addstr(6, 25, "Heading:")
                screen.addstr(7, 25, str(imu["heading"]).rjust(8), curses.color_pair(1))
                screen.addstr(6, 41, "Pitch:")
                screen.addstr(7, 41, str(imu["pitch"]).rjust(8), curses.color_pair(1))
                screen.addstr(6, 53, "Roll:")
                screen.addstr(7, 51, str(imu["roll"]).rjust(8), curses.color_pair(1))
                screen.addstr(6, 61, "MagCal:")
                if imu["mag"] == 3:
                    screen.addstr(7, 65, "yes", curses.color_pair(1))
                else:
                    screen.addstr(7, 65, "no", curses.color_pair(2))

        elif type(imu) == str:
            screen.addstr(6, 25, str(imu), curses.color_pair(2))
        
        if type(reach) == dict:
            if reach == {}:
                screen.addstr(12, 25, "WAITING ON REACH...", curses.color_pair(2))
            else:
                pass
        elif type(reach) == str:
            screen.addstr(12, 25, reach, curses.color_pair(2))

        if type(iftop) == dict:
            if iftop == {}:
                screen.addstr(18, 25, "WAITING ON IFTOP...", curses.color_pair(2))
            else:
                log = getTail("speed")
                screen.addstr(18, 25, "IP Address:")
                screen.addstr(19, 25, iftop["ip"], curses.color_pair(1))
                screen.addstr(18, 41, "Download:")
                screen.addstr(19, 41, str(iftop["download"]), curses.color_pair(1))
                screen.addstr(18, 53, "Upload:")
                screen.addstr(19, 53, str(iftop["upload"]), curses.color_pair(1))
                screen.addstr(21, 25, "Output:")
                screen.addstr(22, 25, log, curses.color_pair(3))
        elif type(iftop) == str:
            screen.addstr(18, 25, iftop, curses.color_pair(2))

        screen.refresh()

        if keyIn == ord("1"):
            keyIn = 0
            restartProcess("speed")
            iftop = {}
            sleep(.1)

        if keyIn == ord("2"):
            pass
        if keyIn == ord("3"):
            pass

    curses.endwin()
    quit()


# This function is where you add the deepstream record for your screenName
def getDataFromDeepstream():
    global keyIn, screen, iftop, reach, imu
    while True:
        try:
            iftop = get("speed")
        except:
            iftop = "NO_RECORD"
        sleep(.08)
        try:
            reach = get("reach")
        except:
            reach = "NO_RECORD"
        sleep(.08)
        try:
            imu = get("imu")
        except:
            imu = {}
        sleep(.08)
        if keyIn == ord(chr(27)):
            quit()
    
def getTail(screenName):
    path        = json.load(open('pathToTitanRover.json'))
    processes   = json.load(open('processes.json'))
    o = [x for x in processes if x['screenName'] == screenName][0]
    fullPath = str(path["path"]) + str(o["path"])
    p = Popen(["cat", "screenlog.0"], cwd=fullPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    p = p.split("\r\n")
    if len(p) > 2:
        p = p[len(p) - 2]
    else:
        return ""
    return p


def getCharFromUser():
    global keyIn, screen
    while True:
        keyIn = screen.getch()
        if keyIn == ord(chr(27)):
            break
        sleep(.05)
    curses.endwin()
    quit()


t1 = Thread(target=runWindow)
t2 = Thread(target=getDataFromDeepstream)
t3 = Thread(target=getCharFromUser)

t1.start()
t2.start()
t3.start()
