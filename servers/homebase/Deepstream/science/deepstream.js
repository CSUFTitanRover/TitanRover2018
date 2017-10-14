const deepstream = require('deepstream.io-client-js');
const WS_URI = '0.0.0.0:6020';
const client = deepstream(WS_URI);

client.on('error', (error, event, topic) => { });

client.login();

module.exports = {
  client
};
