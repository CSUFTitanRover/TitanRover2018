import simplekml
from time import time
from math import floor
kml = simplekml.Kml()

coordList = []

def addPoint(lat, lon):
    coordList.append((lat, lon))

def saveKML():
    if len(coordList) > 1:
        lin = kml.newlinestring(name="RoverTests", description="This test was done on: " + str(time()), coords=coordList)
        kml.save('Rover-GPS-' + str(int(floor(time()))) + ".kml")
        print("Saved the kml file")
    else:
        print("Not enough GPS points to save to KML")
