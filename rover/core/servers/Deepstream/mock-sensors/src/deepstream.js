const deepstream = require('deepstream.io-client-js');
const { getDeepstreamEndpoints} = require('./util');


let client;

/**
 * Returns a Promise that resolves a deepstream client object.
 */
async function getClient() {
  let endpoint = getDeepstreamEndpoints().websocket

  return new Promise((resolve, reject) => {
    if (client !== undefined) {
      resolve(client);
    } else {
      client = deepstream(endpoint);

      client.on('error', (error, event, topic) => {
        reject(error);
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
}