# Homebase Servers


## WebSocketServerJs would run on a raspberry pi zero W, attached to an xbox360 conrtoller:

-----

### Dependencies for WebSocketServerJs:

xboxdrv runs as a child process within the node application, and the data stream is collected, parsed with a
very long regular expression, then into json format to then send over a web socket (port 8888).  The User Interface
React component will retrieve the data from the socket, at the home base station, and the rover should attach to the same
ip:socket to execute mobility(and or)arm movement.  To install the dependencies for the app navigate into the WebSocketServerJs folder:

```sh
chmod +x install.sh;
sudo ./install.sh;
npm i;

```

To run the application, it needs to be run with superuser privaliges:

```sh

sudo node app.js;

```
