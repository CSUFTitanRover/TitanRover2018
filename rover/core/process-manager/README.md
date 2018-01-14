# Process Manager

The process manager is a work in progress

## Setup

In order to add your python script to the master startup process, you need to modify the process.json file.
Here is how the **processes.json** file should look for your process:

```json
[
    {
        "path": "/TitanRover2018/rover/core/servers/ArduinoSocketServer/",
        "python": "python",
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
        "path": "/TitanRover2018/rover/core/servers/reach/",
        "python": "python",
        "screenName": "reach",
        "script": "reach.py"
    }

]
```
The *path* in this **processes.json** file is the path to your python script.

The *python* is which version of python will be running your script.  default *python* will run python2.7

The *screenName* is the name of the screen session your script will run under.  This needs to be **unique** and
it should also match the name of your deepstream record.

The *script* is the full name of your python script.

-----

In order for your scripts to run properly, you need to set the **pathToTitanRover.json** file to something like this:

```json
{ "path": "/home/pi" }
```

Be sure to leave out a trailing slash.  My personal **pathToTitanRover.json** file looks like this, and yours might vary:

```json
{ "path": "/home/audstanley/Documents" }
```
This is because my Titan Rover 2018 file is in my Documents folder.

now, you can run the setup:

```sh
sudo python setup.py
```

This will install all dependencies except for deepstream, which you can find how to install [here](https://github.com/CSUFTitanRover/TitanRover2018/tree/master/rover/core/servers/Deepstream/ds-server#universal-method-to-install-and-run-deepstream)

If you want to add your deepstream records to the process manager get in contact with [me](https://titanrover.slack.com/messages/audstanley/), 
or feel free to look at the main.py in this process manager folder.
