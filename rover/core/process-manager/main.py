from os import system
from deepstream import get, post
import sys
from time import sleep
import curses
from threading import Thread
global keyIn, screen, iftop, reach, imu
iftop = {}
reach = {}
imu = {}
keyIn = 0
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
    return input

def execute_cmd(cmd_string):
    system("clear")
    a = system(cmd_string)
    print ""
    if a == 0:
        print "Command executed correctly"
    else:
        print "Command terminated with error"
    raw_input("Press enter")
    print ""

def runWindow():
    global keyIn, screen, iftop, imu, reach
    
    while keyIn != ord(chr(27)):
        screen = curses.initscr()
        screen.clear()
        screen.border(0)
        screen.addstr(1, 2, "Titan Rover CLI Process Manager", curses.color_pair(1))
        screen.addstr(2, 6, "To restart a process, type the number of the listed process", curses.color_pair(2))
        screen.addstr(4, 4, "Process List:")
        screen.addstr(6, 6, "1 - imu:")
        screen.addstr(9, 6, "2 - reach:")
        screen.addstr(12, 6, "3 - iftop: ")
        #screen.addstr(10, 6, str(keyIn))

        
        if type(imu) == dict:
            if imu == {}:
                pass
            else:
                screen.addstr(6, 25, "Heading:")
                screen.addstr(7, 25, str(imu["heading"]).rjust(8), curses.color_pair(1))
                screen.addstr(6, 41, "Pitch:")
                screen.addstr(7, 41, str(imu["pitch"]).rjust(8), curses.color_pair(1))
                screen.addstr(6, 53, "Roll:")
                screen.addstr(7, 51, str(imu["roll"]).rjust(8), curses.color_pair(1))
                screen.addstr(6, 61, "MagCal:")
                if imu["mag"] == 3:
                    screen.addstr(7, 66, "yes", curses.color_pair(1))
                else:
                    screen.addstr(7, 66, "no", curses.color_pair(2))
        elif type(imu) == str:
            screen.addstr(6, 25, str(imu), curses.color_pair(2))
        
        if type(reach) == dict:
            if reach == {}:
                pass
            else:
                pass
        elif type(reach) == str:
            screen.addstr(9, 25, reach, curses.color_pair(2))

        if type(iftop) == dict:
            if iftop == {}:
                screen.addstr(12, 25, "LOADING", curses.color_pair(2))
            else:
                screen.addstr(12, 25, "IP Address:")
                screen.addstr(13, 25, iftop["ip"], curses.color_pair(1))
                screen.addstr(12, 41, "Download:")
                screen.addstr(13, 41, str(iftop["download"]), curses.color_pair(1))
                screen.addstr(12, 53, "Upload:")
                screen.addstr(13, 53, str(iftop["upload"]), curses.color_pair(1))
        elif type(iftop) == str:
            screen.addstr(12, 25, iftop, curses.color_pair(2))

        screen.refresh()

        if keyIn == ord("1"):
            get_param("what's up?")
            curses.endwin()
        if keyIn == ord("2"):
            pass
        if keyIn == ord("3"):
            pass

    curses.endwin()
    quit()

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