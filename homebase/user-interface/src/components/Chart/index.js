/** TODO:
 * Allow new data to be loaded by first setting data as []
 * Ability to scroll back and forth, and adjust window
 * Ability to change the chart legend
 * Use withStyles?
 *  FIXME:
 * Scroll position gets messed up when tab is switched
 * Auto cull based off of chart width and number of ticks
 */

import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

import Button from 'material-ui/Button';
import Select from 'material-ui/Select';
import { MenuItem } from 'material-ui/Menu';

import c3 from 'c3';
import 'c3/c3.css';

const chartTypes = ['line', 'spline', 'step', 'bar', 'area'];
const flowDuration = 100;

export default class Chart extends Component {
  static propTypes = {
    chartName: PropTypes.string.isRequired,
    yLabel: PropTypes.string,
    chartType: PropTypes.string,
    maxPoints: PropTypes.number,
    data: PropTypes.arrayOf(PropTypes.object),
    timestampFormat: PropTypes.string,
    tickFormat: PropTypes.string,
    culling: PropTypes.oneOfType([PropTypes.bool, PropTypes.shape({ max: PropTypes.number })]),
  };

  static defaultProps = {
    yLabel: 'data',
    chartType: 'line',
    data: [],
    maxPoints: 8,
    timestampFormat: '%Y-%m-%dT%H:%M:%S.%LZ',
    tickFormat: '%H:%M:%S',
    culling: false,
  };

  scrollPos = this.props.maxPoints * -1;
  chart = null;
  dataPoints = 0;
  chartRef = null;
  state = { active: true, chartType: this.props.chartType };

  // Create the C3 chart after mount
  componentDidMount() {
    // Extract applicable keys
    const keys = Object.keys(this.props.data[0] || {});
    const graphValues = keys.filter(value => (value !== 'timestamp'));

    // Bind the chart to the element in chartRef, and load it with the data
    this.chart = c3.generate({
      bindto: this.chartRef,
      data: {
        json: this.props.data,
        keys: { value: graphValues, x: 'timestamp' },
        xFormat: this.props.timestampFormat, // TODO: time zone
      },
      axis: {
        x: {
          type: 'timeseries',
          tick: {
            format: this.props.tickFormat,
            culling: this.props.culling,
          },
        },
        y: {
          label: this.props.yLabel,
        },
      },
    });
  }

  // If the props are changed, update the C3 chart
  componentWillReceiveProps(newProps) {
    // TODO: Use load instead of flow if data was previously empty
    // TODO: Reset if data is empty

    // Return if real-time data is inactive
    if (!this.state.active) {
      return;
    }

    // Extract applicable keys
    const keys = Object.keys(newProps.data[0] || {});
    const graphValues = keys.filter(value => (value !== 'timestamp'));
    this.scrollPos += newProps.data.length;

    // Add the new data to the chart and scroll to a new position
    this.chart.flow({
      json: newProps.data,
      keys: { value: graphValues, x: 'timestamp' },
      duration: flowDuration,
      to: this.scrollPos < 0 ? 0 : undefined,
    });
  }

  // Enable/disable real-time data
  handleClick = () => {
    this.setState(prevState => ({ active: !prevState.active }));
  }

  // Change chart type when a different chart is selected
  handleSelect = (e) => {
    const type = e.target.value;

    this.setState({
      chartType: type,
    });

    this.chart.transform(type);
  }

  render() {
    return (
      <Paper style={{ backgroundColor: '#FFFADD' }}>
        <Grid
          container
          spacing={0}
          style={{ flexWrap: 'nowrap', padding: 16, overflowX: 'hidden' }}
        >
          {/* Left side - options pane */}
          <Grid item xs>
            <Paper style={{ height: '100%' }}>
              <Grid
                container
                direction={'column'}
                align={'center'}
                justify={'center'}
                style={{ height: '100%' }}
              >
                {/* Options pane title */}
                <Grid item style={{ flexGrow: '1' }}>
                  <Typography type={'title'}>Chart Options</Typography>
                </Grid>

                {/* Real-time data button */}
                <Grid item>
                  <Button
                    raised
                    onClick={this.handleClick}
                    color={this.state.active ? 'primary' : 'default'}
                  >
                    {this.state.active ? 'Listening' : 'Not listening'}
                  </Button>
                </Grid>

                {/* Drop down menu */}
                <Grid item>
                  <Select value={this.state.chartType} onChange={this.handleSelect}>
                    {chartTypes.map(type =>
                      <MenuItem value={type} key={type}>{type}</MenuItem>,
                    )}
                  </Select>
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Right side - chart */}
          <Grid item container direction={'column'} align={'center'} xs={10}>
            {/* Chart title */}
            <Grid item>
              <div><Typography type={'headline'}>{this.props.chartName}</Typography></div>
            </Grid>

            {/* The chart */}
            <Grid item style={{ width: '100%' }}>
              <div ref={(elem) => { this.chartRef = elem; }} />
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}
