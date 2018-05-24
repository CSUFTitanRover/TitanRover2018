import React, { Component } from 'react';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';
import WaypointList from '../WaypointList/';

class CurrentWaypointsList extends Component {
  state = { data: [] }

  handleNewPayload = (data) => {
    this.setState({ data: data.pp.reverse() });
  }

  renderWaypointList = (data) => {
    if (data.length === 0) {
      return null;
    }
    return <WaypointList data={data} waypointListType="previousPoints" />;
  }

  render() {
    const { data } = this.state;

    return (
      <DeepstreamRecordProvider
        recordPath="rover/previousPoints"
        onNewPayload={this.handleNewPayload}
      >
        {() => this.renderWaypointList(data)}
      </DeepstreamRecordProvider>
    );
  }
}

export default CurrentWaypointsList;
