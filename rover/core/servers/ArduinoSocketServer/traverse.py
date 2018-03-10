# AutonomousCore module example
from autonomousCore import *
myDriver = Driver()

# CSUF test coordinates
points = [(33.880407973, -117.882214469), (33.880408452, -117.882214337)]

# Drives to each point in a list
for point in points:
    myDriver.goTo(point)

# Rotates Rover to face given heading
myDriver.rotateToHeading(315)

# Set min/max forward speeds
myDriver.setMinMaxFwdSpeeds(35, 45)

# Calculate GPS point based on current GPS coordinate, heading and Distance
crd = (33.882727498, -117.883965627)
heading = 0
distance = 100
pt = myDriver.calcuateGps(crd, heading, distance)

# Calculate the spiral points to travel
radius = 400        # 400 Cm --> 4 Mt
spilist = myDriver.spiralPoints(pt, radius)

# Travel all the points in the spilist(In Concentric Circles) 
while len(spilist) > 0:
    myDriver.goTo(spilist[-1])
    spilist.pop()
