/* eslint-disable react/no-multi-comp */

import React, { Component } from 'react';

const deepstream = require('deepstream.io-client-js');
const appSettings = require('../app-settings.json');

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
 * Wraps a higher-order component around the passed component that
 * connects to a deepstream record and listens for changes in selected
 * state objects.
 *
 * WrappedComponent: the inner component
 * recordName: The deepstream record name
 * states: list of states to listen for changes
 */
export function withDeepstreamState(WrappedComponent, clientType = 'rover', recordName, states) {
  return class DeepStreamWrapper extends Component {
    constructor(props) {
      super(props);

      // Get the deepstream client, then get the record
      getClient(clientType).then((result) => {
        this.client = result;
        this.record = this.client.record.getRecord(recordName);
        this.record.subscribe(this.handleDataChange, true);
      });
    }

    componentDidMount() {
      // Start polling for changes to state
      this.intervalID = setInterval(this.tick, 20);
    }

    componentWillUnmount() {
      // Stop ticking and discard the subscribe event
      clearInterval(this.intervalID);
      this.record.discard();
    }

    client = null;
    record = null;
    wrapped = null;
    intervalID = null;
    recordedState = {};
    acceptChanges = false;

    updateData = (data, callback) => {
      if (!this.wrapped || !this.record) {
        return;
      }

      // Only use records that are in the states argument
      const newState = {};
      states.forEach((val) => {
        newState[val] = data[val];
      });

      // If the two states are different, execute the callback
      if (states.some(key => newState[key] !== this.recordedState[key])) {
        callback(newState);
      }

      // Update the recorded state
      this.recordedState = newState;
    }

    tick = () => {
      // This is to prevent the component from overriding the deepstream value on mount
      if (this.acceptChanges) {
        this.updateData(this.wrapped.state, (newState) => { this.record.set(newState); });
      }
    }

    handleDataChange = (data) => {
      // If the record is not on deepstream, then update the deepstream record
      if (Object.keys(data).length === 0) {
        this.acceptChanges = true;
        return;
      }

      this.updateData(data, (newState) => {
        this.wrapped.setState(newState, () => { this.acceptChanges = true; });
      });
    }

    render() {
      // Use a ref to have access to the state object, and pass through all props
      return (
        <WrappedComponent {...this.props} ref={(comp) => { this.wrapped = comp; }} />
      );
    }
  };
}

/**
 * Wraps a higher-order component around the passed component that
 * connects to a deepstream record and listens for changes in selected
 * prop objects.
 *
 * WrappedComponent: the inner component
 * recordName: The deepstream record name
 */
export function withDeepstreamProps(WrappedComponent, recordName) {
  return class DeepStreamWrapper extends Component {
    constructor(props) {
      super(props);

      this.state = { passedProps: {} };

      // Get the deepstream client, then get the record
      getClient().then((result) => {
        this.client = result;
        this.record = this.client.record.getRecord(recordName);
        this.record.subscribe(this.handleDataChange, true);
      });
    }

    componentWillUnmount() {
      // Discard the subscribe event
      this.record.discard();
    }

    client = null;
    record = null;
    wrapped = null;

    handleDataChange = (data) => {
      this.setState({ passedProps: data });
    }

    render() {
      // Use a ref to have access to the state object, and pass through all props
      return (
        <WrappedComponent {...this.state.passedProps} {...this.props} />
      );
    }
  };
}
