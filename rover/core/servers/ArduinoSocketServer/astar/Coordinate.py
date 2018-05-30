'''
Coordinate.py
Stores coordinate data for Node.py
Titan Rover 2018
Maxfield Wilhoite
'''

class Coordinate:
    
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        
    # Override operators for object comparison
    def __eq__(self, coord):
        return self.lat == coord.lat and self.long == coord.long
        
    def __ne__(self, coord):
        return self.lat != coord.lat or self.long != coord.long
        
    def __sub__(self, coord):
        newCoord = Coordinate(self.lat - coord.lat, self.long - coord.long)
        return newCoord