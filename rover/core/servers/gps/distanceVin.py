from geopy.distance import vincenty
newport_ri = (41.49008, -71.312796)
cleveland_oh = (41.499498, -81.695391)
finalDistance=vincenty(newport_ri, cleveland_oh).meters
finalDistance=finalDistance*100
print(finalDistance)
