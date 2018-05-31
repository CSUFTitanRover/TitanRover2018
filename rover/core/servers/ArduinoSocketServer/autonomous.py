from autonomousCore import *
from astar.Traverse import Traverse
from astar.Coordinate import Coordinate
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
   
    post({'astar' : False}, 'astar')
    trav = Traverse()
    astar = get('astar')
    
    while len(pointsToVisit) > 0:
        if astar['astar']:
            startDict = get('gps')
            start = []
            start.append(startDict['lat']
            start.append(startDict['long']
            goal = Coordinate(pointsToVisit[0], pointsToVisit[1])
            trav.CreateGrid(start, goal)
            coords = get ('coords')
            while len(coords) > 0:
                coord = coords[0]
                coords.remove(coord)
                post({ 'coords' : coords }, 'coords')
                coords = get('coords')
                reply = driver.goTo(coord)
                if reply == -1: # used to quit on the spot in case of emergency
                    break
        else:
            reply = myDriver.goTo(pointsToVisit.pop())
            if reply == -1: # used to quit on the spot in case of emergency
                break
        # update base station

if __name__ == '__main__':
    main()
