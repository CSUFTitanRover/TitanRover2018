const deepstream = require('deepstream.io-client-js');
const { getDeepstreamEndpoints } = require('./util');

// singleton for deepstream clients
// there's only ever going to be 2 clients: 1 for homebase server and 1 for rover server
const clients = {}

/**
 * Returns a Promise that resolves a deepstream client object.
 */
async function getClient(deepstreamServer) {
  let endpoint = getDeepstreamEndpoints()[deepstreamServer].websocket

  return new Promise((resolve, reject) => {
    if (clients[deepstreamServer] !== undefined) {
      resolve(clients[deepstreamServer]);
    } else {
      clients[deepstreamServer] = deepstream(endpoint);

      clients[deepstreamServer].on('error', (error, event, topic) => {
        reject(error);
      });

      clients[deepstreamServer].login({}, (success, data) => {
        if (success) {
          resolve(clients[deepstreamServer]);
        } else {
          reject('Deepstream Client Login was not successful.');
        }
      });
    }
  });
}

module.exports = {
  clients,
  getClient
}