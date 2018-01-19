var ws = new WebSocket('ws://localhost:9014/');
ws.onmessage = function(e) {alert(e.data);};

