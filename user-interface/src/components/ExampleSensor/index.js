import React, { Component } from 'react';
import deepstream from 'deepstream.io-client-js';
import roverSettings from '../../utils/roverSettings.json';

const { URI } = roverSettings.deepstream;

class ExampleSensor extends Component {
  constructor() {
    super();
    this.client = deepstream(URI.ws).login();
  }

  componentDidMount() {
    this.client.on('connectionStateChanged', (state) => {
      console.log(state);
    });
    // this.client.event.subscribe('science/decagon-5TE', (payload) => {
    //   console.log('--------');
    //   console.log('Received new payload...');
    //   console.log(payload);
    //   this.setState({ payload });
    // });
  }

  renderSensorPayload = () => {
    const { payload } = this.state;

    if (payload !== undefined || payload !== null) {
      return (
        Object.entries(payload).map(([key, val]) => (
          <div>`${key}: ${val}`</div>
        ))
      );
    }
    return null;
  }

  render() {
    return (
      <div>
        <h2>Example Sensor</h2>
      </div>
    );
  }
}

export default ExampleSensor;
