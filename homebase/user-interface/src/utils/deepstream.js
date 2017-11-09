import React, { Component } from 'react';

const deepstream = require('deepstream.io-client-js');
const roverSettings = require('./roverSettings.json');

const { rover } = roverSettings.deepstream;
const clients = {}; // singleton

/**
 * Returns a Promise that resolves a deepstream client object.
 *
 * socket: the URL of the deepstream server (defaults to rover.ws)
 */
export function getClient(socket) {
  const url = socket || rover.ws;

  return new Promise((resolve, reject) => {
    if (clients[url] !== undefined) {
      // Return the client associated with this URL
      resolve(clients[url]);
    } else {
      // Create a new deepstream client
      clients[url] = deepstream(url);

      clients[url].on('error', (error, event, topic) => {
        reject(error, event, topic);
      });

      clients[url].login({}, (success) => {
        if (success) {
          resolve(clients[url]);
        } else {
          reject('Deepstream Client Login was not successful.');
        }
      });
    }
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
export function withDeepstreamState(WrappedComponent, recordName, states) {
  return class DeepStreamWrapper extends Component {
    constructor(props) {
      super(props);

      // Get the deepstream client, then get the record
      getClient().then((result) => {
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
