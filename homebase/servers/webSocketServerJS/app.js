/*

  Richard Stanley
  Web socket server for the xbox/xbox360 controllers for any debain linux.
  This was written for the titan rover.

*/

// spawn a child process. Documentation: https://nodejs.org/api/child_process.html
const spawn = require("child_process").spawn;

let app = require("express");
let socket = require("http").Server(app);
let io = require("socket.io")(socket);
//let test = require('./Test.js');

let cData = {}; // cData will be sent over the web socket, just need to define it in scope.
/* 
  This regex will match this string which is the standard output of xboxdrv: 
    X1: 32000 Y1:-32000 X2:-15000 Y2: 15000 du:0 dd:0 dl:0 dr:0 back:0 guide:0 start:0 TL:0 TR:0 A:0 B:0 X:0 Y:0 LB:0 RB:0 LT:255 RT:255
  The regular expression is matched, and an array is created, storing the values as strings which
  gets converted to numbers for JSON parsing on the client end.
  JSON can be parsed easily with many languages.
*/
let r = /X1:\s*(\-?\d{1,5})\s*Y1:\s*(\-?\d{1,5})\s*X2:\s*(\-?\d{1,5})\s*Y2:\s*(\-?\d{1,5})\s*du:([01])\s+dd:([01])\s+dl:([01])\s+dr:([01])\s+back:([01])\s+guide:([01])\s+start:([01])\s+TL:([01])\s+TR:([01])\s+A:([01])\s+B:([01])\s+X:([01])\s+Y:([01])\s+LB:([01])\s+RB:([01])\s+LT:\s*(\d{1,3})\s+RT:\s*(\d{1,3})/;
let rConf = /Your Xbox\/Xbox360 controller should now be available/;
try {
  const xboxdrv = spawn("xboxdrv", ["--detach-kernel-driver"]);
  // This function captures the data from stdout (standard out). The "data" is a buffer.
  xboxdrv.stdout.on("data", data => {
    // run regex against the string after convering the buffer to a string.
    // this returns an array
    let capture = r.exec(data.toString());
    let available = rConf.exec(data.toString());
    if (available !== null)
      console.log("The Xbox controller has been attached");
    else if (available === null && capture === null)
      console.log("No attachment");
    // make sure the capture array is not null, else instantiate an empty arr.  Node will crash
    // if we were to try to run the map function on an uninstantiated array.
    let arr = capture !== null ? capture.map(e => parseInt(e)) : [];
    // store the array in an key value paired object.
    let obj = {
      X1: arr[1],
      Y1: arr[2],
      X2: arr[3],
      Y2: arr[4],
      du: arr[5],
      dd: arr[6],
      dl: arr[7],
      dr: arr[8],
      back: arr[9],
      guide: arr[10],
      start: arr[11],
      TL: arr[12],
      TR: arr[13],
      A: arr[14],
      B: arr[15],
      X: arr[16],
      Y: arr[17],
      LB: arr[18],
      RB: arr[19],
      LT: arr[20],
      RT: arr[21]
    };
    // update cData
    cData = obj;
    //console.log(cData);
  });

  // log any stderr output
  xboxdrv.stderr.on("data", data => {
    console.log("stderr:", data.toString());
  });

  // when process has ended, output the exit code
  xboxdrv.on("close", code => {
    console.log(`child process exited with code ${code}`);
    const kernelReset = spawn("rmmod", ["xpad"]);
    kernelReset.stderr.on("data", data => {
      console.log("stderr:", data.toString());
    });
    clearTimeout(timoutId);
  });
} catch (e) {
  console.log(e);
}

// imports, then start the websocket on port 8888
let launchSocket = () => {
  // Start the server
  socket.listen(8888, function() {
    console.log(
      "============ Server is up and running on port: ",
      socket.address().port,
      "============="
    );
  });

  // Socket.io is going to be handling all the emits events that the UI needs.
  io.on("connection", function(socketClient) {
    console.log("Client Connected: " + socketClient.id);
    setInterval(() => {
      socketClient.emit("broadcast", cData);
    }, 7);
  });

  process.on("SIGINT", function() {
    console.log("\n####### Server shutting down #######\n");
    process.exit();
  });
};

let timoutId = setTimeout(launchSocket, 3000);
