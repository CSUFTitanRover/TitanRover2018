import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import isEqual from 'lodash.isequal';
import c3 from 'c3';
import 'c3/c3.css';

/**
 * The main goal for the FlowChart is to be aware that data will
 * be pumped into it by being hooked up into Deepstream via a Higher Order Component,
 * which means as data comes in the chart will flow and append the new data.
 */
class FlowChart extends Component {
  static propTypes = {
    /** An optional chart name that displays a title on the chart. */
    chartName: PropTypes.string,
    /** Defines the type of chart it renders as.
     *
     * @see Available types can be found here: http://c3js.org/reference.html#data-type
    */
    chartType: PropTypes.string,
    /** This is the data point that will be constantly
     * updated via Deepstream or some other measure. */
    currentDataPoint: PropTypes.object,
    /** A valid timestamp format for each data point. */
    timestampFormat: PropTypes.string,
    /** A valid timestamp format each point's x-tick will render as. */
    tickFormat: PropTypes.string,
    /** Determines if the number of x-ticks are limited when rendered.  */
    culling: PropTypes.oneOfType([PropTypes.bool, PropTypes.shape({ max: PropTypes.number })]),
    /** The y-axis label name */
    yLabel: PropTypes.string,
    /** Controls the number of data points rendered on the chart at a given time. */
    maxPointsRendered: PropTypes.number,
    /** The animation time in ms it takes to flow in a new data point. */
    flowDuration: PropTypes.number,
  }

  static defaultProps = {
    chartName: null,
    chartType: 'line',
    currentDataPoint: null,
    timestampFormat: '%Y-%m-%dT%H:%M:%S.%LZ',
    tickFormat: '%H:%M:%S',
    culling: false,
    yLabel: 'data',
    maxPointsRendered: 8,
    flowDuration: 100,
  };

  scrollPos = this.props.maxPointsRendered * -1;
  state = { data: [] }

  componentDidMount() {
    const { chartType, timestampFormat, tickFormat, culling, yLabel } = this.props;
    const initialDataKeyNames = [];
    const initialData = [];

    // check if data was passed on the initial mount
    // if (data.length > 0) {
    //   const k = Object.keys(data[0]);
    //   dataKeyNames = k.filter(keyName => (keyName !== 'timestamp'));
    // }
    // we do not need to grab data keys when we mount
    // since we can assume this chart will start empty
    // and fill up as new data points are passed into it

    const chartDataProps = {
      type: chartType,
      json: initialData,
      keys: {
        x: 'timestamp',
        value: initialDataKeyNames,
      },
      xFormat: timestampFormat,
    };

    const chartAxisProps = {
      x: {
        type: 'timeseries',
        tick: {
          format: tickFormat,
          culling,
        },
      },
      y: {
        label: yLabel,
      },
    };

    // generate our c3 chart
    this.chart = c3.generate({
      bindto: this.chartRef,
      data: chartDataProps,
      axis: chartAxisProps,
    });
  }

  componentWillReceiveProps(nextProps) {
    // we need to check if changes occured for
    // 'data' and 'chartType' to apply those
    // changes to the chart using the c3 api

    const { chartType, flowDuration, currentDataPoint } = this.props;

    if (chartType !== nextProps.chartType) {
      // change the chart type via c3
      this.chart.transform(nextProps.chartType);
    }

    // flow a new data point into the chart and save it.
    // we can check for equality here since it's only 2 objects
    // to compare versues an entire array of objects
    if (isEqual(currentDataPoint, nextProps.currentDataPoint)) {
      this.chart.flow({
        json: currentDataPoint,
        keys: {
          value: this._extractDataPointKeys(currentDataPoint),
          x: 'timestamp',
        },
        duration: flowDuration,
        to: this.scrollPos < 0 ? 0 : undefined,
      });
    }
  }

  _extractDataPointKeys = dataPoint => Object.keys(dataPoint).filter(keyName => (keyName !== 'timestamp'))

  renderChartName = () => {
    const { chartName } = this.props;

    if (chartName) {
      return (
        <Grid item xs={12} align="center" >
          <Typography variant="title">{chartName}</Typography>
        </Grid>
      );
    }
    return null;
  }

  render() {
    return (
      <Grid container direction="column">
        {this.renderChartName()}
        <Grid item xs={12}>
          <div ref={(elem) => { this.chartRef = elem; }} />
        </Grid>
      </Grid>
    );
  }
}

export default FlowChart;
