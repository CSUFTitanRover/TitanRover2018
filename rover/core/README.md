AtlasCore
======

### Quick Reference
core.py is a script ran at boot(handled by linux) that will manage the different process-managers(modes) the rover will have. 

AtlasCore.py is a command line tool used to interact with core.py when the UI is not present and connected to the rover.

### Rover modes
Currently the rover has 4 modes described as the following:
1. Manual - This mode is defualt for the rover unless the UI is connected to core.py. This allows for you to use a physical remote connected to the rover wirelessly or wired.
2. Remote - This mode is default when core.py is connected to the UI. This allows for remote command done via joystick. 
3. Autonomous - This mode is activated during the autonomous task, it will activate all additional sensors/processes needed to run in autonomy mode
4. Science - This mode is activated during the science task, it will activate all additional sensors/processes needed to run the science attachment.

Modes will refer to a specific process manager that will start any necesary processes needed to be successful at that task. Modes can be forced regardless of what attachment is on the rover, each process manager should be handling any exceptions allowing for the mode to run flawlessly.

### Local Commands for atlasCore
* help - lists all of the interactive core commands
* connect - attempts to connect to atlas core
* restart - restarts the active connection to atlas core
* quit - quits the atlasCore terminal program

### Core Commands for atlasCore
* whichMode - returns which mode the core manager is in(Autonomy, Science, Remote or Manual(Default))
* setModeAutonomy - sets the core's mode to autonomy
* setModeScience - sets the core's mode to science
* setModeRemote - sets the core's mode to Remote
* setModeManual - sets the core's mode to Manual(Default)
* setModeDefault - sets the core's mode to Manual(Default) when connected to atlasCore, if the UI is connected it will default to Remote
* resetCurrent - resets the core, returning to it's current mode on reboot
* resetCore - resets the core, returning it to default
* getVersion - gets the core's version number

### Version Methodology
atlasCore will always have the same functionality as the UI, therefore it is equivalent to what commands the UI can send to core.py. Therefore core.py and atlasCore.py must have the same version numbers to be fully compatable. 

Currently the atlasCore will be at version 1.0.0 as of 11/21/2017. Any additions major additions will iterate the second number, smaller additions on major additions will iterate the third number. 

core.py is on version 0.0.4 to reflect it's current compatibility with atlasCore. We will follow the same versioning for core.py, for example implementing setModeManual would iterate the second number. Once all commands are implemented in core.py up to the current release of atlasCore the version numbers will match.

### Process-Managers
For more information, read the Process-Managers README. 