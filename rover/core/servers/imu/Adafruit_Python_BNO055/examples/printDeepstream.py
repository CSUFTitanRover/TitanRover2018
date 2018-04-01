from deepstream import get
from time import sleep
ip = "10.42.0.1"

while True:
    try:
        data = get('imu')
        print(data)
        sleep(.05)
    except:
        print("problem connecting to deepstream")