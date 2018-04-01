from deepstream import get, post
from time import sleep

while True:
    try:
        iftop = get("speed")
        sleep(.1)
        mode = get("mode")
        print(iftop)
        print(mode)
        sleep(1)
    except:
        print("problem connecting to deepstream")