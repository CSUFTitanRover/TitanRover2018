const deepstream = require('deepstream.io-client-js');
const appSettings = require('../../../user-interface/src/appSettings.json');

const { homebase } = appSettings.deepstream;
let homebaseClient; // singleton for deepstream client connected to the homebase

/**
 * Returns a Promise that resolves a deepstream client object.
 */
function getClient() {
  return new Promise((resolve, reject) => {
    if (homebaseClient !== undefined) {
      resolve(homebaseClient);
    } else if (homebaseClient === undefined) {
      // we need to get the deepstream client
      const endpoint = homebase.ws;
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