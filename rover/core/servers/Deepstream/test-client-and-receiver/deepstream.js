const deepstream = require('deepstream.io-client-js');
const WS_URI = '0.0.0.0:4020';
let client; // singleton

/**
 * Returns a ready ds client
 */
function getClient() {
  return new Promise((resolve, reject) => {
    if (client !== undefined) {
      resolve(client);
    } else {
      client = deepstream(WS_URI);

      client.on('connectionStateChanged', (connectionState) => {
        console.log('Deepstream Client connectionStateChanged: ', connectionState);
      });

      client.on('error', (error, event, topic) => {
        console.log(error, event, topic);
      });

      client.login({}, (success, data) => {
        if (success) {
          resolve(client);
        } else {
          reject('Deepstream Client Login was not successful.');
        }
      });
    }
  });
}

module.exports = {
  getClient
};