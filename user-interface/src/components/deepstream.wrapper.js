import React, { Component } from 'react';
import deepstream from 'deepstream.io-client-js';
import roverSettings from '../utils/roverSettings.json';

const { URI } = roverSettings.deepstream;

// Deepstream
const withDeepstream = (WrappedComponent, event) =>
  class DeepstreamWrapper extends Component {
    constructor(props) {
      super(props);

      this.client = deepstream(URI.ws).login();
      this.state = { data: null };
    }

    componentDidMount() {
      // TODO: Unsubscribe from event on unmount
      // also: data validation?

      this.client.event.subscribe(event, (payload) => {
        this.setState({
          data: JSON.parse(payload),
        });
      });
    }

    render() {
      return (
        <WrappedComponent data={this.state.data} {...this.props} />
      );
    }
  };


export default withDeepstream;
