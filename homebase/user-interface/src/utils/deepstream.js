/* eslint-disable react/no-multi-comp */

import React, { Component } from 'react';
import PropTypes from 'prop-types';

const deepstream = require('deepstream.io-client-js');
const appSettings = require('../app-settings.json');

const { rover } = appSettings.deepstream;
let client; // singleton list of clients for each server URL

/**
 * Returns a Promise that resolves a deepstream client object.
 *
 * @param {string} endpoint: the URL of the deepstream server (defaults to rover.ws)
 */
export function getClient(endpoint = rover.ws) {
  return new Promise((resolve, reject) => {
    if (client !== undefined) {
      resolve(client);
    } else {
      client = deepstream(endpoint);

      client.on('error', (error) => {
        reject(error);
      });

      client.login({}, (success) => {
        if (success) {
          resolve(client);
        } else {
          reject('Deepstream Client Login was not successful.');
        }
      });
    }
  });
}

// Closes the client connection to deepstream
export function closeClient() {
  client.close();
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

/** A Higher Order Component that uses the renderProps technique to provide deepstream updates to
 * a child component. The DeepstreamRecordProvider listens for a record being updated and will
 * transfer new updates to a child component.
 *
 * In order to use this HOC, provide a function as the child component.
 * There are 4 parameters that are then passed to the
 * function: currentDataPoint, subscribed, subscribeToUpdates, unsubscribeToUpdates
 *
 * @see RealtimeChart.js for a working example
 */
export class DeepstreamRecordProvider extends Component {
  static propTypes = {
    /** Can be a single or multiple record paths to subscribe to */
    recordPath: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.arrayOf(PropTypes.string)],
    ).isRequired,
    children: PropTypes.func.isRequired,
  }

  client = null
  record = null
  records = null // used if multiple records are being subscribed to
  multipleRecords = false
  state = {
    /** The provider has all subscriptions active or not */
    subscribed: false,
    /** A single object holding all of the latest payloads
     * (e.g. aggregated data between multiple subscriptions)
     */
    currentDataPoint: null,
  }

  async componentDidMount() {
    try {
      const { recordPath } = this.props;
      this.client = await getClient();

      if (typeof recordPath === 'string') {
        this.record = await getRecord(this.client, recordPath);
      } else if (recordPath instanceof Array) {
        this.records = [];
        this.multipleRecords = true;

        const resolvedRecords = await Promise.all(
          recordPath.map(path => getRecord(this.client, path)),
        );

        resolvedRecords.forEach((record) => {
          this.records.push(record);
        });
      }

      // automatically start subscribing to changes
      this.subscribeToUpdates();
    } catch (e) {
      console.error(e);
    }
  }

  _subscribe = (record) => {
    record.subscribe((payload) => {
      let { currentDataPoint } = this.state;

      // overwrite the current data with the new payload
      // this takes care of having subscriptions to multiple records
      // and combing the data into 1 single object
      currentDataPoint = { ...currentDataPoint, ...payload };

      this.setState({ currentDataPoint });
    });
  }

  _unsubscribe = (record) => {
    record.discard();
  }

  subscribeToUpdates = () => {
    const { subscribed } = this.state;

    if (!subscribed) {
      this.setState({ subscribed: true });

      if (!this.multipleRecords) {
        this._subscribe(this.record);
      } else {
        this.records.forEach((record) => {
          this._subscribe(record);
        });
      }
    }
  }

  unsubscribeToUpdates = () => {
    const { subscribed } = this.state;

    if (subscribed) {
      this.setState({ subscribed: false });

      if (!this.multipleRecords) {
        this._unsubscribe(this.record);
      } else {
        this.records.forEach((record) => {
          this._unsubscribe(record);
        });
      }
    }
  }

  componentWillUnmount() {
    if (!this.multipleRecords) {
      this._unsubscribe(this.record);
    } else {
      this.records.forEach((record) => {
        this._unsubscribe(record);
      });
    }
  }

  render() {
    const { currentDataPoint, subscribed } = this.state;
    const { children } = this.props;

    return (
      children(currentDataPoint, subscribed, this.subscribeToUpdates, this.unsubscribeToUpdates)
    );
  }
}

/** A Higher Order Component that uses the renderProps technique to provide deepstream updates to
 * a child component. The DeepstreamSensorProvider listens for an event being published to and will
 * transfer new updates to a child component.
 *
 * In order to use this HOC, provide a function as the child component.
 * There are 4 parameters that are then passed to the
 * function: currentDataPoint, subscribed, subscribeToUpdates, unsubscribeToUpdates
 *
 * @see RealtimeChart.js for a working example
 */
export class DeepstreamSensorProvider extends Component {
  static propTypes = {
    subscriptionPath: PropTypes.string.isRequired,
    children: PropTypes.func.isRequired,
  }

  client = null
  recordList = null

  state = { subscribed: false, currentDataPoint: null }

  async componentDidMount() {
    try {
      this.client = await getClient();
      // automatically start subscribing to changes
      this.subscribeToUpdates();
    } catch (e) {
      console.error(e);
    }
  }

  handleUpdates = (newDataPoint) => {
    this.setState({ currentDataPoint: newDataPoint });
  }

  subscribeToUpdates = () => {
    const { subscribed } = this.state;
    const { subscriptionPath } = this.props;

    if (!subscribed) {
      this.setState({ subscribed: true });
      this.client.event.subscribe(subscriptionPath, this.handleUpdates);
    }
  }

  unsubscribeToUpdates = () => {
    const { subscriptionPath } = this.props;
    const { subscribed } = this.state;

    if (subscribed) {
      this.setState({ subscribed: false });
      client.event.unsubscribe(subscriptionPath, this.handleUpdates);
    }
  }

  componentWillUnmount() {
    this.unsubscribeToUpdates();
  }

  render() {
    const { currentDataPoint, subscribed } = this.state;
    const { children } = this.props;

    return (
      children(currentDataPoint, subscribed, this.subscribeToUpdates, this.unsubscribeToUpdates)
    );
  }
}
