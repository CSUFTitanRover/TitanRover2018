import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import c3 from 'c3';
import 'c3/c3.css';

/**
 * This is a simple chart that allows data to be loaded into it.
 * The main usage for this DefaultChart is showing data that is stored
 * in the database that was collected from sensors after our tasks.
 */
class DefaultChart extends Component {
  static propTypes = {
    /** An optional chart name that displays a title on the chart. */
    chartName: PropTypes.string,
    /** Defines the type of chart it renders as.
     *
     * @see Available types can be found here: http://c3js.org/reference.html#data-type
    */
    chartType: PropTypes.string,
    /** The chart data that will be loaded. */
    data: PropTypes.arrayOf(PropTypes.object),
    /** A valid timestamp format for each data point. */
    timestampFormat: PropTypes.string,
    /** A valid timestamp format each point's x-tick will render as. */
    tickFormat: PropTypes.string,
    /** Determines if the number of x-ticks are limited when rendered.  */
    culling: PropTypes.oneOfType([PropTypes.bool, PropTypes.shape({ max: PropTypes.number })]),
    /** The y-axis label name */
    yLabel: PropTypes.string,
  }

  static defaultProps = {
    chartName: null,
    chartType: 'line',
    data: [],
    timestampFormat: '%Y-%m-%dT%H:%M:%S.%LZ',
    tickFormat: '%H:%M:%S',
    culling: false,
    yLabel: 'data',
  };

  componentDidMount() {
    const { data, chartType, timestampFormat, tickFormat, culling, yLabel } = this.props;
    let dataKeyNames = [];

    // check if data was passed on the initial mount
    if (data.length > 0) {
      // use the first data point to get the data keys
      const k = Object.keys(data[0]);
      dataKeyNames = k.filter(keyName => (keyName !== 'timestamp'));
    }

    const chartDataProps = {
      type: chartType,
      json: data,
      keys: {
        x: 'timestamp',
        value: dataKeyNames,
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

    const { chartType } = this.props;

    if (chartType !== nextProps.chartType) {
      // change the chart type via c3
      this.chart.transform(nextProps.chartType);
    }

    // unfortunately it can take a lot of resources to compare
    // the old vs new data since we'd have to check for equality
    // for every object inside the data array (esp. if there is
    // a lot of items in the array) so the best solution right now
    // is just to load the "new" data in without checking
    // for differences and let React take care
    // of optimizing when to render.
    this.chart.load({
      unload: true,
      json: nextProps.data,
    });
  }

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

export default DefaultChart;
