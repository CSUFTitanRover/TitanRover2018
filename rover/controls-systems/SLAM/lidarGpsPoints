from deepstream import get
import math

def calculateGps(origin, lidarDeg, distance):
        '''
        Description:
            Uses current GPS point, lidar degree output, and distance to object (cm) to calculate a new GPS point
        Args:
            Heading, current GPS point tuple (lat, lon), and distance (cm)
        Returns:
            Tuple: (lat, lon)
        '''

        try:
            currentHeading = get("imu")["heading"]
        except:
            print("Heading error")

        heading = (lidarDeg + currentHeading) % 360
        
        if type(heading) != float or type(heading) != int or type(distance) != int or type(distance) != float:
            raise TypeError("Only Int or Float allowed")

        if type(origin) != tuple:
            raise TypeError("Only Tuples allowed")

        heading = math.radians(heading)
        radius = 6371 # km
        dist =  distance / 100000.0
        lat1 , lon1 = origin

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        lat2 = math.asin( math.sin(lat1)*math.cos(dist/radius) + math.cos(lat1)*math.sin(dist/radius)*math.cos(heading))
        lon2 = lon1 + math.atan2(math.sin(heading)*math.sin(dist/radius)*math.cos(lat1), math.cos(dist/radius)-math.sin(lat1)*math.sin(lat2))

        lat2 = round(math.degrees(lat2), 9)
        lon2 = round(math.degrees(lon2), 9)

        return (lat2, lon2)
