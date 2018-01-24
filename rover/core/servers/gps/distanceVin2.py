import geopy
from geopy.distance import VincentyDistance

# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers

origin = geopy.Point(56.3,85.2)
#distance given in meters
destination = VincentyDistance(kilometers=115).destination(origin, 110)

lat2, lon2 = destination.latitude, destination.longitude
print(lat2,lon2)
