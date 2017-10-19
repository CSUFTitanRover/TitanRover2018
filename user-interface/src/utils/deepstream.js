const deepstream = require('deepstream.io-client-js');
const roverSettings = require('./roverSettings.json');

const { rover } = roverSettings.deepstream;
let client; // singleton

/**
 * Returns a ready ds client
 */
function getClient() {
  return new Promise((resolve, reject) => {
    if (client !== undefined) {
      resolve(client);
    } else {
      client = deepstream(rover.ws);

      client.on('connectionStateChanged', (connectionState) => {
        console.log('Deepstream Client connectionStateChanged: ', connectionState);
      });

      client.on('error', (error, event, topic) => {
        console.log(error, event, topic);
      });

      client.login({}, (success, data) => {
        if (success) {
          console.log('Successfully logged in', data);
          resolve(client);
        } else {
          reject('Deepstream Client Login was not successful.');
        }
      });
    }
  });
}

module.exports = {
  getClient,
};
