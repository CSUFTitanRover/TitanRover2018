'''
Traverse.py 
Autonomous traversal using AStar.py for path generation
Titan Rover 2018
Maxfield Wilhoite
'''

from AStar import AStar
from Node import Node
from Coordinate import Coordinate
from deepstream import get, post


class Traverse:
    def __init__(self):
        self.nodes = {}
        post({'astar' : True}, 'astar')
        

    # Generate a grid of nodes based on the start and goal gps coordinates
    def CreateGrid(self, start, goal):
        start.lat = float(int(round(start.lat * 100000,0)))
        start.long = float(int(round(start.long * 100000,0)))
        goal.lat = float(int(round(goal.lat * 100000, 0)))
        goal.long = float(int(round(goal.long * 100000, 0)))
        step = Coordinate(0,0)
        step.lat = int(abs(goal.lat - start.lat))
        step.long = int(abs(goal.long - start.long))
        if step.lat < 50:
            step.lat = 50
        if step.long < 50:
            step.long = 50
        newNode = Node(start)
        nodeKey = str(newNode.position.lat) + str(newNode.position.long)
        self.nodes[nodeKey] = newNode
        
        for x in range((-step.lat - 10), (step.lat + 11)):
            for y in range((-step.long - 10), (step.long + 11)):
                newCoord = Coordinate(start.lat,start.long)
                newNode = Node(newCoord)
                newNode.position.lat +=  x
                newNode.position.long += y
                nodeKey = str(newNode.position.lat) + str(newNode.position.long)
                if nodeKey not in self.nodes:
                    self.nodes[nodeKey] = newNode
        return self.nodes
        
    # Call the A* algorithm and post it to deepstream
    def CalcPath(self, start, goal):
        astar = AStar(self.nodes)
        print('Calculating Shortest Path')
        coords = astar.GetPath(start,goal)
        if coords == None:
            post({'astar' : False}, 'astar')
            coords = {}
        #print(coords)
        post({ 'coords' : coords }, 'coords')
        
    # Mark a node not clear (clear=False). This will be called when LIDAR detects obstacles.
    def SetBlocked(self, coord):
        newCoord = []
        newCoord.append(float(int(round(coord[0] * 100000,0))))
        newCoord.append(float(int(round(coord[1] * 100000,0))))
        coordKey = str(newCoord[0]) + str(newCoord[1])
        self.nodes[coordKey].clear = False

# Main for function testing
def main():
    #start = Coordinate(33.88507, -117.88328)    # ~1km
    #start = Coordinate(33.88132, -117.88344)    # ~.1km
    start = Coordinate(33.00000, -117.00000)    # test data
    print('Start: ', start.lat, start.long)

    #goal = Coordinate(33.87421, -117.88961)     # ~1km
    #goal = Coordinate(33.88161, -117.88239)     # ~.1km
    goal = Coordinate(33.00005, -117.00005)     # test data
    print('Goal: ', goal.lat, goal.long)

    # Will be in calling script
    trav = Traverse()
    nodes = trav.CreateGrid(start, goal)
    #print(nodes)
    #print('----------------')
    print('Grid Created, Calculating Path')
    trav.CalcPath(start, goal)
    print('Shortest Path posted to deepstream')
    
    coord = (33.00003,-117.00003) # test data
    trav.SetBlocked(coord)
    trav.CalcPath(start, goal)
    
'''
if __name__ == "__main__":
    main()
'''
    
# Test cases
'''
startKey = str(start.lat) + str(start.long)
print(nodes[startKey])

goalKey = str(goal.lat) + str(goal.long)
print(nodes[goalKey])

print(trav.nodes)
print(nodes['3387404-11788848'].position.lat, nodes['3387404-11788848'].position.long)
print(nodes['3387404-11788849'].position.lat, nodes['3387404-11788849'].position.long)
print(nodes['0,0'])

step = start - goal
print(step.lat, step.long)
step.lat = int(round(step.lat * 100000,0))
step.long = int(round(step.long * 100000,0))
print(step.lat,step.long)
test = Coordinate(370, 613)
print(step == test)

step.lat = 5
step.long = 5

for x in range(-step.lat, step.lat + 1):
    for y in range(-step.long, step.long + 1):
        if x != 0 or y != 0:
            print(x,y)
'''