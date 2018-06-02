'''
AStar.py 
A* algorithm to generate shortest path from start to goal
Titan Rover 2018
Maxfield Wilhoite
'''

from Node import Node
from Coordinate import Coordinate

class AStar:
    def __init__(self, nodes):
        self._nodes = nodes
        
    # Main A* algorithm to generate a list of tuples that represent the shortest path. The tuples are lat,long pairs.
    def GetPath(self, start, goal):
        startKey = str(start.lat) + str(start.long)
        self.__openList = []
        self.__closedList = []
        self.__finalPath = []
        currentNode = self._nodes[startKey]
        currentNode.GScore = 0
        self.__openList.append(currentNode)
        goalKey = str(goal.lat) + str(goal.long)
        while (len(self.__openList) > 0):
            for x in range(-1,2):
                for y in range(-1,2):
                    neighborPos = Coordinate(currentNode.position.lat - x, currentNode.position.long - y)
                    neighborKey = str(neighborPos.lat) + str(neighborPos.long)
                    if neighborPos != currentNode.position and neighborKey in self._nodes:
                        if self._nodes[neighborKey].clear:
                            if abs(x - y) == 1:
                                gScore = 10
                            else:
                                if not self.ConnectedDiagonally(currentNode, self._nodes[neighborKey]):
                                    continue
                                gScore = 14
                            neighborNode = self._nodes[neighborKey]
                            if neighborNode in self.__openList:
                                if currentNode.GScore + gScore < neighborNode.GScore:
                                    neighborNode.CalcValues(currentNode, self._nodes[goalKey], gScore)
                            elif neighborNode not in self.__closedList:
                                self.__openList.append(neighborNode)
                                neighborNode.CalcValues(currentNode, self._nodes[goalKey], gScore)
            self.__openList.remove(currentNode)
            self.__closedList.append(currentNode)
            if len(self.__openList) > 0:
                self.__openList.sort(key=lambda n: n.FScore)
                currentNode = self.__openList[0]
            if currentNode == self._nodes[goalKey]:
                while currentNode.position != start:
                    newTuple = (currentNode.position.lat / 100000, currentNode.position.long / 100000)
                    self.__finalPath.insert(0, newTuple)
                    currentNode = currentNode.parent
                return self.__finalPath
        return None
        
    # Disallow diagonal movements when a node is adjacent to an obstacle
    def ConnectedDiagonally(self, currentNode, neighborNode):
        direction = neighborNode.position - currentNode.position
        first  = Coordinate(currentNode.position.lat + direction.lat, currentNode.position.long)
        second = Coordinate(currentNode.position.lat, currentNode.position.long - direction.long)
        third = Coordinate(currentNode.position.lat - direction.lat, currentNode.position.long)
        fourth = Coordinate(currentNode.position.lat, currentNode.position.long + direction.long)
        firstKey = str(first.lat) + str(first.long)
        secondKey = str(second.lat) + str(second.long)
        thirdKey = str(third.lat) + str(third.long)
        fourthKey = str(fourth.lat) + str(fourth.long)
        if not self._nodes[firstKey].clear:
            return False
        if not self._nodes[secondKey].clear:
            return False
        if not self._nodes[thirdKey].clear:
            return False
        if not self._nodes[fourthKey].clear:
            return False
        return True