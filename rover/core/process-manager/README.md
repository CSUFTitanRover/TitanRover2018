# Process Manager & Dependencies

The process manager is a work in progress
and can be found [here](https://github.com/CSUFTitanRover/TitanRover2018/tree/master/rover/core/process-manager)
![Process Manager](https://github.com/CSUFTitanRover/TitanRover2018/blob/master/rover/core/process-manager/gif/TitanRoverProcessManager.gif?raw=true)




## Setup

In order to add your python script to the master startup process, you need to modify the process.json file.
Here is an example of the **processes.json** file where each process is an object in the array:

```json
[
    {
        "path": "/TitanRover2018/rover/core/process-manager/motionConf/",
        "python": "sudo",
        "screenName": "motion",
        "script": "motion"
    },
    {
        "path": "/TitanRover2018/rover/core/servers/ArduinoSocketServer/",
        "python": "python3.4",
        "screenName": "mobility",
        "script": "mobility.py"
    },
    {
        "path": "/TitanRover2018/rover/core/servers/iftop/",
        "python": "python",
        "screenName": "speed",
        "script": "iftop.py"
    },
    {
        "path": "/TitanRover2018/rover/controls-systems/mobility/GNSS/",
        "python": "python",
        "screenName": "reach",
        "script": "emlidreach.py"
    },
    {
        "path": "/TitanRover2018/rover/controls-systems/mobility/GNSS/",
        "python": "python",
        "screenName": "reachSocketServer",
        "script": "socketServer.py"
    }
]
```
There are three processes in this example above. All you need to do is add your process to the file.

> The ***path*** in this **processes.json** file is the path to your python script.

> The ***python*** is which version of python will be running your script.  default *python* will run python2.7

> The ***screenName*** is the name of the screen session your script will run under.  This needs to be **unique** and it should also match the name of your deepstream record. (preferably)

> The ***script*** is the full name of your python script.

-----

In order for your scripts to run properly, you need to **ALSO change** the **pathToTitanRover.json** file to something like this:

```json
{ "path": "/home/pi" }
```

Be sure to leave out a trailing slash.  **My** personal **pathToTitanRover.json** file looks like this, and yours will vary:

```json
{ "path": "/home/audstanley/Documents" }
```
This is because my Titan Rover 2018 file is in my Documents folder.

now, you can run the setup:

```sh
sudo python setup.py
```

This will install all dependencies **except for deepstream**, which you can find how to install [here](https://github.com/CSUFTitanRover/TitanRover2018/tree/master/rover/core/servers/Deepstream/ds-server#universal-method-to-install-and-run-deepstream)

If you want to add your deepstream records to the process manager get in contact with [me](https://titanrover.slack.com/messages/audstanley/), 
or feel free to look at the main.py in this process manager folder.


## Motion
Motion will automatically install with the **setup.py** script and be added to the startup process along
with the other startup processes.  This may not be something you want, because motion takes control of 
your web camera, if you are on a laptop.  If you don't want this, you can simply remove the line that references motion in your **/etc/crontab** file. The line should look something like this:

```sh
@reboot root cd /home/audstanley/Documents/TitanRover2018/rover/core/process-manager/motionConf/ && screen -dmLS motion && screen -S motion -X stuff "sudo motion \015";
``` 

if you want to get motion running on startup again, you can simply rerun:

```sh
sudo python setup.py
```
and motion will be added to the startup process again.

## Screen
Let's talk a little about how all of these startup precesses all work.  Your script gets added to **/etc/crontab** and
it's added to a screen session.  If you already ran the **setup.py** as sudo, then you currently
have screen installed on your machine.  In short, screen is like bash, but where you can go into
a screen session, or pop out of a screen session, and your script keeps running in the background.
This becomes immensely helpful when debugging, since your stdout, and stderr can be viewed at any time.
If your script is failing for any reason, then it's really easy to find out how and why by going into the 
screen session and viewing errors, and your stdout prints to console. Another great thing about screen is that screen has the option to save log files of all of the output from your session.

Since all the screen sessions are being called in the startup process as root, you will first need to
be root in order to view them. 

```sh
sudo su;
```

Now that you are root, you can view the screen sessions:

```sh
screen -ls;
```

If you see something like *No sockets found*, then your screen sessions have not started yet, and the easiest way to
start those sessions is to reboot. (assuming you have run the setup.py already)

If you want to create your own screen sessions (in detached mode):

```sh
screen -dmS someScreenNameThatYouLike
```

To attach to a screen session:

```sh
screen -x someScreenNameThatYouLike;
# or to attach to a TitanRover process:
screen -x speed; # which is a session for you to be able to view your upload download speed
# most likely this session will show a python error, and you can trouble shoot how to fis this error.
# You will likely need to change the file /TitanRover2018/rover/core/servers/iftop/iftop.py
# and edit the variable:
# interface = "wlp3s0"
# on line 10, to an interface that you have on your machine.
# once you change that, iftop.py will work on startup (which is running in the screen session "speed")
```





If you want to leave the session **without** stopping your script, you can gracefully leave the session
by holding **Ctrl** **A** then lift up on the **A** key, and hit **D** (Holding **Ctrl** the whole time)

These are some of the basics, for more info read the docs:

```sh
man screen;
# or
screen --help;
```
