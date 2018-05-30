'''
Node.py
Stores node data for AStar.py
Titan Rover 2018
Maxfield Wilhoite
'''

from Coordinate import Coordinate

class Node:
    
    def __init__(self, position):
        self.position = position
        self.clear = True
        self.GScore = 0
        self.HScore = 0
        self.FScore = 0
        
    # Calculate the GScore, HScore, and FScore of the node
    def CalcValues(self, parent, goal, gScore):
        self.parent = parent
        self.GScore = parent.GScore + gScore
        self.HScore = (abs(self.position.lat - goal.position.lat) + abs(goal.position.long - self.position.long))
        self.FScore = self.GScore + self.HScore