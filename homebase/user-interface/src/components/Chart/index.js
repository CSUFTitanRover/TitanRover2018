/** TODO:
 * Allow new data to be loaded by first setting data as []
 * Ability to scroll back and forth, and adjust window
 * Ability to change the chart legend
 *  FIXME:
 * Scroll position gets messed up when tab is switched
 * Auto cull based off of chart width and number of ticks
 */

import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import Select from 'material-ui/Select';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import { MenuItem } from 'material-ui/Menu';
import { withStyles } from 'material-ui/styles';
import grey from 'material-ui/colors/grey';
import blueGrey from 'material-ui/colors/blueGrey';
import c3 from 'c3';
import 'c3/c3.css';

const chartTypes = ['line', 'spline', 'step', 'bar', 'area'];
const flowDuration = 100;

const styles = theme => ({
  root: {
    backgroundColor: grey[100],
  },
  appbar: {
    backgroundColor: blueGrey[100],
  },
  toolbarItemSpacing: {
    marginLeft: theme.spacing.unit * 2,
    marginRight: theme.spacing.unit * 2,
  },
});

class Chart extends Component {
  static propTypes = {
    chartName: PropTypes.string.isRequired,
    yLabel: PropTypes.string,
    chartType: PropTypes.string,
    maxPoints: PropTypes.number,
    data: PropTypes.arrayOf(PropTypes.object),
    timestampFormat: PropTypes.string,
    tickFormat: PropTypes.string,
    culling: PropTypes.oneOfType([PropTypes.bool, PropTypes.shape({ max: PropTypes.number })]),
    classes: PropTypes.object.isRequired,
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
    const { data } = this.props;
    let keys;
    let graphValues;

    if (data.length > 0) {
      // Extract applicable keys
      keys = Object.keys(data);
      graphValues = keys.filter(value => (value !== 'timestamp'));
    }
    // Bind the chart to the element in chartRef, and load it with the data
    this.chart = c3.generate({
      bindto: this.chartRef,
      data: {
        json: data,
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
    const { classes, chartName } = this.props;
    const { active, chartType } = this.state;

    return (
      <Grid
        container
        spacing={16}
        className={classes.root}
        direction="column"
      >
        <Grid item xs={12}>
          <AppBar position="static" color="default" elevation={1} className={classes.appbar}>
            <Toolbar disableGutters>
              <Typography variant="title" className={classes.toolbarItemSpacing}>Chart Options</Typography>

              <Button
                className={classes.toolbarItemSpacing}
                variant="raised"
                onClick={this.handleClick}
                color={active ? 'primary' : 'default'}
              >
                {active ? 'Listening' : 'Not listening'}
              </Button>

              <Select
                value={chartType}
                onChange={this.handleSelect}
                className={classes.toolbarItemSpacing}
              >
                {chartTypes.map(type =>
                  <MenuItem value={type} key={type}>{type}</MenuItem>,
                )}
              </Select>
            </Toolbar>
          </AppBar>
        </Grid>

        <Grid item xs={12}>
          <Grid container>
            <Grid item xs={12} align="center">
              <Typography variant="title">{chartName}</Typography>
            </Grid>
            <Grid item xs={12}><div ref={(elem) => { this.chartRef = elem; }} /></Grid>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

// export default withStyles(styles)(Chart);

export default () => (<div>Hi</div>);
