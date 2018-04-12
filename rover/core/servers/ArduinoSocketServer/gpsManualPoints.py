from deepstream import get, post
import math
from time import sleep


global points
global points1
global mode
global lat1
global lon1
global reach
mode = "manual"
points = []
reach = {}
lat1 = 0
lon1 = 0


def getFromDeepstream():
    global points, points1
    while True:
        reach = get('gps')
        mode = get('mode')
        points1 = get('gpsManual')
        if points1 != {} and len(points1['points']) != len(points):
            points = points1['points']
        if type(reach) == dict:
            storeToDeepstream(reach)
        sleep(0.1)


def storeToDeepstream(reach):
    global Points, mode, lat1, lon1
    lat2, lon2 = reach['lat'], reach['lon']
    if distance((lat1, lon1), (lat2, lon2)) > 5.0 and reach['sde'] < 10 and reach['sdn'] < 10 and reach['fix'] and mode == "manual":
        if len(points) < 30:
            points.append((lat2, lon2))
        else: 
            del points[0]
            points.append((lat2, lon2))
    
    post({"points" : points}, "gpsManual", 'localhost')
    
    lat1 = lat2
    lon1 = lon2


def distance(origin, destination):
    print("getting into Distance")
    a1, b1 = origin
    a2, b2 = destination
    radius = 6371 # km

    da = math.radians(a2-a1)
    db = math.radians(b2-b1)
    a = math.sin(da/2) * math.sin(da/2) + math.cos(math.radians(a1)) \
        * math.cos(math.radians(a2)) * math.sin(db/2) * math.sin(db/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d * 1000

getFromDeepstream()