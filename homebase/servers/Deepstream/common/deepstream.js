const deepstream = require('deepstream.io-client-js');
const appSettings = require('../../../user-interface/src/appSettings.json');
const { rover, homebase } = appSettings.deepstream;
let roverClient; // singleton for deepstream client connected to the rover
let homebaseClient; // singleton for deepstream client connected to the homebase

/**
 * Returns a Promise that resolves a deepstream client object.
 *
 * @param {string} clientType: the type of deepstream client to use. Can be "rover" or "homebase"
 */
function getClient(clientType) {
  let endpoint;
  let client;
  switch (clientType) {
    case 'rover':
      endpoint = rover.ws;
      client = roverClient;
      break;
    case 'homebase':
      endpoint = homebase.ws;
      client = homebaseClient;
      break;
    default:
      throw new SyntaxError('clientType must be either "rover" or "homebase".');
  }


  return new Promise((resolve, reject) => {
    if (client !== undefined) {
      resolve(client);
    } else if (client === undefined) {
      // we need to get the deepstream client with the clientType in mind
      if (clientType === 'rover') {
        roverClient = deepstream(endpoint);

        roverClient.on('error', (error) => {
          reject(error);
        });

        roverClient.login({}, (success) => {
          if (success) {
            resolve(roverClient);
          } else {
            reject('Deepstream Client Login was not successful.');
          }
        });
      } else {
        homebaseClient = deepstream(endpoint);
        homebaseClient.on('error', (error) => {
          reject(error);
        });

        homebaseClient.login({}, (success) => {
          if (success) {
            resolve(homebaseClient);
          } else {
            reject('Deepstream Client Login was not successful.');
          }
        });
      }
    }
  });
}

// Closes the homebase client connection to deepstream
function closeHomebaseClient() {
  homebaseClient.close();
}

/**
 *
 * @param {DeepstreamClient} dsClient - working deepstream client
 * @param {string} path - path to where the record lvies
 * @returns {DeepstreamRecord} - a ready record
 */
function getRecord(dsClient, path) {
  return new Promise((resolve) => {
    dsClient.record.getRecord(path).whenReady((record) => {
      resolve(record);
    });
  });
}

/**
 *
 * @param {DeepstreamClient} dsClient - working deepstream client
 * @param {string} path - path to where the record lvies
 * @returns {DeepstreamRecord} - a ready record
 */
function getRecordList(dsClient, path) {
  return new Promise((resolve) => {
    dsClient.record.getList(path).whenReady((list) => {
      resolve(list);
    });
  });
}

module.exports = {
  getClient,
  closeHomebaseClient,
  getRecord,
  getRecordList
}