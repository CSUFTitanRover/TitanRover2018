from autonomousCore import *
from deepstream import get

# Autonomous module object
myDriver = Driver()

global pointsToVisit
pointsToVisit = {}

def stop():
    '''
    Description:
        Used to exit the current goTo function indefinitely.
    '''
    try:
        post({"stop" :  True}, "stop")
    except:
        print("DS post error")

def pause():
    '''
    Description:
        Toggles between pause state.
    '''
    try:
        post({"pause" : True}, "pause")
    except:
        print("DS pause error")

    def quit():
        '''
    Description:
        Used to quit further autonomous traversal.
    '''
    try:
        post({"quit'" : True}, "quit")
    except:
        print("DS quit error")

def main():
    try:
        pointsToVisit = get('points')
    except:
        print("GPS points error in DS")

    while len(points) > 0:
        reply = myDriver.goTo(points.pop())
        if reply == -1: # used to quit on the spot in case of emergency
            break
        # update base station

if __name__ == '__main__':
    main()
