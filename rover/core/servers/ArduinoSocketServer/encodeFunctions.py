from codecs import encode, decode
from base64 import b64decode
from time import time

# Number to Encoded Hex
def n2a(num):
  num = hex(num)[2:].rstrip("L")
  if len(num) % 2:
    num = "0" + num
  return encode(decode(num, 'hex'), 'base64').decode()

# Lat to Encoded Hex
def lat2a(lat):
  lat = hex(lat)[2:].rstrip("L")
  if len(lat) % 2:
    lat = "0" + lat
  return encode(decode(lat, 'hex'), 'base64').decode()

# Lon to Encoded Hex (removes negative)
def lon2a(lon):
  lon = hex(lon)[2:].rstrip("L")
  if len(lon) % 2:
    lon = "0" + lon
  return encode(decode(lon, 'hex'), 'base64').decode()

# Encoded Hex back to Number
def a2n(alpha):
  print(alpha)
  n = b64decode(alpha).hex()
  print('a2n', n)
  n = int(n, 16)
  return n

# Encoded Lat back to Number
def a2lat(lat):
  n = b64decode(lat).hex()
  n = int(n, 16)
  return n

# Encoded Lon Back to Number (converts back to negative)
def a2lon(lon):
  n = b64decode(lon).hex()
  n = int(n, 16)
  return n * -1

# Encodes tha Lat and Lon
def encodedLatLon(t):
  if type(t) == tuple and len(t) == 2:
    lat = lat2a(int(t[0] * 1000000000))
    lon = lon2a(int(t[1] * -1000000000))
    return str(str(lat) + ',' + str(lon)).replace('\n', '')
  else:
    return None 

def decodeLatLon(s):
  s = s.split(',')
  if len(s) == 2:
    t = (float(a2lat(s[0])) / 1000000000, float(a2lon(s[1])) / 1000000000)
    #print(t)
    return t
  else:
    return None

# Encodes Epoch Time in milliseconds
def encodedEpoch():
  ms = int(round(time(), 3) * 1000)
  #print(ms)
  return str(n2a(ms))

# Decodes Epoch Time
def decodeEpoch(s):
  return float(a2n(s)) / 1000


"""  

# Section to test numbers:

e = encodedEpoch()
print(e)
print(decodeEpoch(e))

ll = (33.783859375, -117.483958304) 
print(ll)
e = encodedLatLon(ll)
print("encoded: ", e)
d = decodeLatLon(e)
print("decodeLatLon:", d)


print("epoch: " + str(time()))
print("encodedVersion: " + encodedEpoch())
v = encodedEpoch()
print(v)
print("decoded: " + str(decodeEpoch(v)))


"""
