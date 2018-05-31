import isEmpty from 'lodash.isempty';

const deepstream = require('deepstream.io-client-js');
const appSettings = require('../appSettings.json');

const { rover, homebase } = appSettings.deepstream;
let roverClient; // singleton for deepstream client connected to the rover
let homebaseClient; // singleton for deepstream client connected to the homebase

/**
 * Returns a Promise that resolves a deepstream client object.
 *
 * @param {string} clientType: the type of deepstream client to use. Can be "rover" or "homebase"
 */
export function getClient(clientType) {
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

// Closes the rover client connection to deepstream
export function closeRoverClient() {
  roverClient.close();
}

// Closes the homebase client connection to deepstream
export function closeHomebaseClient() {
  homebaseClient.close();
}

/**
 *
 * @param {DeepstreamClient} dsClient - working deepstream client
 * @param {string} path - path to where the record lvies
 * @returns {DeepstreamRecord} - a ready record
 */
export function getRecord(dsClient, path) {
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
export function getRecordList(dsClient, path) {
  return new Promise((resolve) => {
    dsClient.record.getList(path).whenReady((list) => {
      resolve(list);
    });
  });
}

/**
 * Initializes deepstream state to match up with an initial component state and vice versa
 * @param {DeepstreamClient} dsClient - a valid, connected deepstream client
 * @param {string} recordPath - the record path which is to be synced with
 * @param {Object} componentInitialState - the initial state to submit for syncage
 * @return {Promise<string>} Promise<string> - returns a string with the success message
 */
export function syncInitialRecordState(dsClient, recordPath, componentInitialState) {
  return new Promise((resolve, reject) => {
    dsClient.record.has(recordPath, (error, hasRecord) => {
      if (error) {
        reject(error);
      } else if (!hasRecord) {
        dsClient.record.setData(recordPath, componentInitialState);
        resolve('Successfully initialized record with component state.');
      } else {
        // get a snapshot of the current record data to "update" this component's state
        dsClient.record.snapshot(recordPath, (e, data) => {
          // there is a bug that I assume is due to the drag source of Golden Layout
          // but when the component is being dragged it initializes the deepstream
          // record with an empty object as its data so we must double check
          if (e) {
            reject(e);
          } else if (isEmpty(data)) {
            // sync the initial state up to the deepstream record (state -> deepstream)
            dsClient.record.setData(recordPath, componentInitialState);
            resolve('Successfully initialized record with component state.');
          } else {
            // sync deepstream record down to component state (deepstream -> state)
            this.setState(data);
            resolve('Successfully synced up component state with the existing record state.');
          }
        });
      }
    });
  });
}
