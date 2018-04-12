from sys import version_info
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
  alpha = alpha.replace('\n', '')
  if version_info[0] < 3:
    n = b64decode(alpha)
    n = int(n.encode('hex'), 16)
  else:
    n = b64decode(alpha).hex()
    n = int(n, 16)
  return n

# Encoded Lat back to Number
def a2lat(lat):
  if version_info[0] < 3:
    n = b64decode(lat)
    n = int(n.encode('hex'), 16)
  else:
    n = b64decode(lat).hex()
    n = int(n, 16)
  return n

# Encoded Lon Back to Number (converts back to negative)
def a2lon(lon):
  if version_info[0] < 3:
    n = b64decode(lon)
    n = int(n.encode('hex'), 16)
  else:
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
    return t
  else:
    return None

# Encodes Epoch Time in milliseconds
def encodedEpoch():
  ms = int(round(time(), 3) * 1000)
  return str(n2a(ms)).replace('\n', '')

# Decodes Epoch Time
def decodeEpoch(s):
  return float(a2n(s)) / 1000

"""
# Section to test numbers:

ll = (33.783859375, -117.483958304) 
print(ll)
e = encodedLatLon(ll)
print("encodedLatLon:", e)
d = decodeLatLon(e)
print("LatLon Decoded:", d)

v = encodedEpoch()
print(v)
print("epoch: " + str(time()))
print("encodedVersionOfEpoch: " + v)
print("decoded: " + str(decodeEpoch(v)))

"""
