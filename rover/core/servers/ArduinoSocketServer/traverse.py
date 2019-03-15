# AutonomousCore module example
from autonomousCore import *
myDriver = Driver()

# CSUF test coordinates
points = [(33.88239, -117.883568)] #, (33.88239 , -117.883568), (33.882513, -117.88.607751), (33.882434, -117.8835028), (33.88245 , -117.883660)]

#33.88234 , -117.883603
#33.88245 , -117.883660
#33.88239 , -117.883568
#33.882434, -117.8835028


# good point 33.882489475, -117.883671113

# Drives to each point in a list
for point in points:
    myDriver.goTo(point)

# Rotates Rover to face given heading
#myDriver.rotateToHeading(315)

# Set min/max forward speeds
#myDriver.setMinMaxFwdSpeeds(35, 45)

# Calculate GPS point based on current GPS coordinate, heading and Distance
#crd = (33.882727498, -117.883965627)
#heading = 0
#distance = 100
#pt = myDriver.calcuateGps(crd, heading, distance)

# Calculate the spiral points to travel
#radius = 400        # 400 Cm --> 4 Mt
#spilist = myDriver.spiralPoints(pt, radius)

# Travel all the points in the spilist(In Concentric Circles)
#while len(spilist) > 0:
    #myDriver.goTo(spilist[-1])
    #spilist.pop()
