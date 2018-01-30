# Deepstream Data to Four Oleds

First, you will need the dependency "screen" to launch these scripts on startup:


```sh
sudo apt-get install screen;
```

This project consists of four oleds attached to our rover.  The python scripts on launch will consist of
oLed1.py
oLed2.py
oLed3.py
oLed4.py

These scripts can be launched via a crontab.


```sh
sudo vim /etc/crontab
```

create these lines in crontab:


```
@reboot root /usr/bin/screen -dmS imu && /usr/bin/screen -X stuff 'cd /home/pi/TitanRover2018/rover/core/servers/oLed/ && /usr/bin/python oLed1.py\015';
@reboot root /usr/bin/screen -dmS imu && /usr/bin/screen -X stuff 'cd /home/pi/TitanRover2018/rover/core/servers/oLed/ && /usr/bin/python oLed2.py\015';
@reboot root /usr/bin/screen -dmS imu && /usr/bin/screen -X stuff 'cd /home/pi/TitanRover2018/rover/core/servers/oLed/ && /usr/bin/python oLed3.py\015';
@reboot root /usr/bin/screen -dmS imu && /usr/bin/screen -X stuff 'cd /home/pi/TitanRover2018/rover/core/servers/oLed/ && /usr/bin/python oLed4.py\015';
```

As of right now, only oLed1.py has been written, though the code is mostly reuseable.

For information on the process of assigning udev rules to each serial to usb device attached, as well as find the schematics for printing the custom 4 oLed board, please read schematics/README.md

For the u8glib library necessary to flash the 4 arduinos, you need to transfer: 
arduino oLed1/U8glib_Arduino-1.19.1
to your Arduino Library folder.

Each arduino pin 10, is the RX pin for the data stream coming from each associated python script.

oLed1.py -> arduino1

oLed2.py -> arduino2

oLed3.py -> arduino3

oLed4.py -> arduino4

Each arduino and oled will share 5v power and ground from the usb attached to 

oLed1 -> arduino1 (CP2102 - serial number: 1000)
