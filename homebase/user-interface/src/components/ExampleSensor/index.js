import React, { Component } from 'react';
import { getClient } from '../../utils/deepstream';

class ExampleSensor extends Component {
  state = { payload: {} };

  async componentDidMount() {
    this.client = await getClient();

    this.client.event.subscribe('science/decagon-5TE', (payload) => {
      this.setState({ payload: JSON.parse(payload) });
    });
  }

  render() {
    const { payload } = this.state;

    return (
      <div>
        <h2>Example Sensor</h2>

        {Object.entries(payload).map(([key, val]) => (
          <div key={`${key}-${val}`}>
            {key}: {val}
          </div>
        ))}
      </div>
    );
  }
}

export default ExampleSensor;
