import React, { Component } from 'react';
import Chart from './index';
import { DeepstreamRecordProvider } from '../../utils/deepstream';

class ChartWithDeepstream extends Component {
  totalData = []

  renderChart = (data) => {
    this.totalData.push(data);
    return (
      <Chart data={this.totalData} {...this.props} />
    );
  }

  render() {
    return (
      <DeepstreamRecordProvider recordPath="science/decagon" >
        {this.renderChart}
      </DeepstreamRecordProvider>
    );
  }
}

export default ChartWithDeepstream;
