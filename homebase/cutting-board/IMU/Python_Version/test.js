var sys = require('sys');

var start = new Date();

var spawn = require("child_process").spawn;
var process = spawn('python',["IMU_Acc_Mag_Gyro.py"]);

process.stdout.on('data', function (data){
	var valueReturn = data.toString();

	var arr = valueReturn.split(",");

	///////Error checking output - Disable in final use/////////
	if(1)
		for(var i=0;i<arr.length;i++) {
    			console.log(arr[i]);
		}

	var end = new Date() - start;
	console.log("Execution time: ", end);
	////////////////////////////////////////////////////////////
});

