import requests as r
from time import sleep
from subprocess import Popen
import subprocess

# Writing to the file is done in the process-manager folder, so urls[1] should be the file to write to
# relative to the process-manager folder path. 
urls = [    
            #("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/setup.py", "setup.py"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/processes.json", "processes.json"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/udev/99-usb-serial.rules", "udev/99-usb-serial.rules"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/motionConf/motion.conf", "motionConf/motion.conf"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/motionConf/thread1.conf", "motionConf/thread1.conf"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/motionConf/thread2.conf", "motionConf/thread2.conf"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/motionConf/thread3.conf", "motionConf/thread3.conf"),
            ("https://raw.githubusercontent.com/CSUFTitanRover/TitanRover2018/master/rover/core/process-manager/motionConf/thread4.conf", "motionConf/thread4.conf"),
]

try:
    for e in urls:
        res = r.get(e[0]).text
        print(e)
        print(res)
        f = open(e[1], 'w')
        f.write(res)
        f.close()
        sleep(.8)
    o = Popen(["python", "setup.py"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    print(o)
except:
    pass
