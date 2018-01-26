# Motion Cameras

## Basic Html/JS/CSS to control our motion cameras

In order to control the cameras, you need to install the chrome extension:
[CORS Toggle](https://chrome.google.com/webstore/detail/cors-toggle/jioikioepegflmdnbocfhgmpmopmjkim?hl=en)

The reason you need this extension, is because chrome doesn't like you sending commands to ip addresses or something. If you want to test without the CORS extension, go for it. If you have errors in your chrome console, it's likely because you need the extension running.


Running the app is simple.  Open the html in your browser, in the IP address section put the address of the rover:
192.168.1.2
then click the change button.

If you are testing the code on your laptop, then you'll attach to localhost.

If you want to see your webcam, make sure you run the setup.py first under:
```
/TitanRover/rover/core/process-manager/setup.py
# then you will need to edit your thread1.conf file
sudo nano /etc/motion/thread1.conf;
```

Look for the line:
```
videodevice /dev/SOMETHING
```

change to:
```
videodevice /dev/video0
```

This **should** be your webcamera.
The video defaults to an aweful bitrate.
Click the buttons in the html document to change quality.

have fun
