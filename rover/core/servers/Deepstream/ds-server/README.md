# Rover Deepstream Server

This is the main directory for the official Deepstream server that will run on our Rover's Computer.

Ports the DS rover server will listen on:

| Endpoint  | Address | PORT |
| --------- | ------- | ---- |
| Websocket | 0.0.0.0 | 4020 |
| HTTP      | 0.0.0.0 | 4080 |


-----

# Universal Method to install and run deepstream:
This process is **necessary** if you are running deepstream on a raspberry pi, and works on the
raspberry pi as well as any other Linux distro

## FIRST, Make sure you have NodeJs installed:
NodeJs install:

For [**Raspberry pi & Beaglebone ONLY** go here](https://github.com/audstanley/NodeJs-Raspberry-Pi) and copy paste the code block into your cli to install NodeJs on your raspberry pi or beaglebone.

For x86 or x64 Linux use the installers go here do this:

```sh
curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential
````

For [Windows go here](https://github.com/CSUFTitanRover/TitanRover2018/blob/master/rover/core/servers/Deepstream/ds-server/README.md#windows-guide)

For [Mac go here](https://github.com/CSUFTitanRover/TitanRover2018/tree/master/rover/core/servers/Deepstream/ds-server#mac-guide) 

## The Linux Guide (raspberry pi, x86 or x64):
After you have successfully installed NodeJs...
### Clone the deepstream project:
I like to keep deepstream in my Documents folder:

```sh
cd ~/Documents/;
git clone https://github.com/deepstreamIO/deepstream.io;
cd deepstream.io/;
git submodule update --init 
npm i;
npm start;
```
At this point, you are running deepstream, but we have some config files in deepstream that we want to edit. First go ahead and crash deepstream ctrl-c.

```sh
# Install pm2 also, which we will need later to start deepstream on startup
sudo npm install pm2 -g;
```


Now after we have also installed pm2, Let's look at the deepstream file tree:

```
├── appveyor.yml
├── ascii-logo.txt
├── benchmarks
├── bin                
├── CHANGELOG.md
├── conf  (file)             
├── dist  (file)             <-- we will launch dist/bin/deepstream on startup with pm2
├── elton-square.png             as well as dist/conf/config.yml
├── jasmine.json
├── jasmine-runner.js
├── LICENSE
├── node_modules
├── package.json
├── package-lock.json
├── protocol
├── README.md
├── scripts
├── src
├── test
├── test-e2e
├── tsconfig.json
└── tslint.json
```

you are going to want to open **dist/conf/config.yml** and edit lines ~21 and ~47:

```
Example of part of the dist/conf/config.yml file...
...
16 connectionEndpoints:
17   websocket:
18     type: default
19     options:
20         # port for the websocket server
21         port: 4020                          # FOR TITANROVER
22         # host for the websocket server
23         host: 0.0.0.0
24         # url path websocket connections connect to
25         urlPath: /deepstream
26         # url path for http health-checks, GET requests to this path will return 200 if deepstream is alive
27         healthCheckPath: /health-check
28         # the amount of milliseconds between each ping/heartbeat message
29         heartbeatInterval: 30000
30         # the amount of milliseconds that writes to sockets are buffered
31         outgoingBufferTimeout: 0
32 
33         # Security
34         # amount of time a connection can remain open while not being logged in
35         # or false for no timeout
36         unauthenticatedClientTimeout: 180000
37         # invalid login attempts before the connection is cut
38         maxAuthAttempts: 3
39         # if true, the logs will contain the cleartext username / password of invalid login attempts
40         logInvalidAuthData: false
41         # maximum allowed size of an individual message in bytes
42         maxMessageSize: 1048576
43   http:
44     type: default
45     options:
46       # port for the http server
47       port: 4080                                # FOR TITANROVER
48       # host for the http server
49       host: 0.0.0.0
50       # allow 'authData' parameter in POST requests, if disabled only token and OPEN auth is
51       # possible
52       allowAuthData: true
53       # enable the authentication endpoint for requesting tokens/userData.
54       # note: a custom authentication handler is required for token generation
55       enableAuthEndpoint: false
56       # path for authentication requests
57       authPath: /auth
58       # path for POST requests
59       postPath: /
60       # path for GET requests
61       getPath: /
...

```

line 21 should be set to this:
```
port: 4020
```
line 47 should be set to this:
```
port: 4080
```
Save the file, and now let's setup deepstream to automatically run on startup.

```sh
# First you will need to bee your root user
sudo su;
# Change into the deepstream.io/dist/bin/ folder:
cd dist/bin/;
# add deepstream to the pm2
pm2 start deepstream --name deepstream;
# save the pm2 settings
pm2 save;
# add the startup process to pm2
pm2 startup;

# Now if you want to check pm2 to see if deepstream is running, just make sure you are root and...
pm2 ls;
```
You should see something like this:

```
┌────────────┬────┬──────┬──────┬────────┬─────────┬────────┬─────┬───────────┬──────┬──────────┐
│ App name   │ id │ mode │ pid  │ status │ restart │ uptime │ cpu │ mem       │ user │ watching │
├────────────┼────┼──────┼──────┼────────┼─────────┼────────┼─────┼───────────┼──────┼──────────┤
│ deepstream │ 0  │ fork │ 1552 │ online │ 0       │ 4h     │ 0%  │ 74.2 MB   │ root │ disabled │
└────────────┴────┴──────┴──────┴────────┴─────────┴────────┴─────┴───────────┴──────┴──────────┘
 Use `pm2 show <id|name>` to get more details about an app

```

If you want to view the logs for deepstream, just sudo su, then you can view deepstream logs:

```
pm2 log deepstream;
```

You should see this:

```
audstanley-G750JM bin # pm2 log deepstream
[TAILING] Tailing last 15 lines for [deepstream] process (change the value with --lines option)
/root/.pm2/logs/deepstream-error-0.log last 15 lines:
/root/.pm2/logs/deepstream-out-0.log last 15 lines:
0|deepstre |  =====================   starting   =====================
0|deepstre | INFO | logger ready: std out/err
0|deepstre | INFO | deepstream version: 4.0.0-beta.2
0|deepstre | INFO | configuration file loaded from ../conf/config.yml
0|deepstre | INFO | authenticationHandler ready: none
0|deepstre | INFO | cache ready: local cache
0|deepstre | INFO | storage ready: noop storage
0|deepstre | INFO | permissionHandler ready: valve permissions loaded from /home/audstanley/Documents/deepstream.io/dist/conf/permissions.yml
0|deepstre | INFO | Listening for websocket connections on 0.0.0.0:4020/deepstream
0|deepstre | INFO | Listening for health checks on path /health-check 
0|deepstre | INFO | connectionEndpoint ready: µWebSocket Connection Endpoint
0|deepstre | INFO | Listening for http connections on 0.0.0.0:4080
0|deepstre | INFO | Listening for health checks on path /health-check
0|deepstre | INFO | connectionEndpoint ready: HTTP connection endpoint
0|deepstre | INFO | Deepstream started
```

Ctrl-C to get out of viewing the log.

```sh
# To log out of root user:
exit;
```
Now you have successfully installed deepstream, and pm2 will launch deepstream
every time your computer starts up. Now you can get and post data to deepstream.
You will need the [deepstream.py](https://github.com/CSUFTitanRover/TitanRover2018/blob/master/rover/core/servers/ArduinoSocketServer/deepstream.py) file in your project's folder to get and post data easily to deepstream.
The deepstream.py file has a dependency called: *requests*, 

Let's install that **NOW**

```sh
sudo apt-get install python-requests
```

Happy coding Titan Rover data to deepstream.




## Windows Guide:
If you are on windows, there are two ways you can install deepstream.
#### Bash on ubuntu on Windows:
Follow [this](https://docs.microsoft.com/en-us/windows/wsl/install-win10) guide first, then you can install NodeJs in bash.
Open the Windows command prompt:

```cmd
bash
```
Then you can follow this [Linux portion of this guide](https://github.com/CSUFTitanRover/TitanRover2018/blob/master/rover/core/servers/Deepstream/ds-server/README.md#clone-the-deepstream-project)

The second method is boring and complex, just get bash on ubuntu on windows.

## Mac Guide:
todo;
