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
import FlowChart from '../FlowChart/';
import { DeepstreamSensorProvider } from '../../utils/deepstream';

/**
 * @see Available types can be found here: http://c3js.org/reference.html#data-type
*/
const chartTypes = [
  'line', 'spline', 'step', 'area', 'area-spline',
  'area-step', 'bar', 'scatter', 'pie', 'donut', 'gauge',
];

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

/** The RealtimeChart hooks up into deepstream and displays sensor data
 * in real-time. All of the props excluding chartType that are valid for FlowChart can be passed
 * to the RealtimeChart since any provided props will be passed down into the FlowChart.
*/
class RealtimeChart extends Component {
  static propTypes = {
    /** An optional chart name that displays a title on the chart. */
    chartName: PropTypes.string,
    /** Material-UI styles object that is passed in via withStyles() */
    classes: PropTypes.object.isRequired,
    /** The subscription path the chart will listen to. */
    subscriptionPath: PropTypes.string.isRequired,
  }

  static defaultProps = {
    chartName: null,
  }

  state = { chartType: 'line' }

  handleChartTypeChange = ({ target }) => {
    const type = target.value;

    this.setState({
      chartType: type,
    });
  }

  toggleDeepstreamListening = (subscribed, subscribeToUpdates, unsubscribeToUpdates) => {
    if (subscribed) {
      unsubscribeToUpdates();
    } else {
      subscribeToUpdates();
    }
  }

  render() {
    const { classes, subscriptionPath } = this.props;
    const { chartType } = this.state;

    // make a copy of props for the flow chart but exclude the chart type and current data point
    // since those are going to be managed by this component directly
    const flowChartProps = { ...this.props };
    delete flowChartProps.chartType;
    delete flowChartProps.currentDataPoint;

    return (
      <DeepstreamSensorProvider subscriptionPath={subscriptionPath}>
        {(currentDataPoint, subscribed, subscribeToUpdates, unsubscribeToUpdates) => (
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
                    onClick={() => {
                      this.toggleDeepstreamListening(
                        subscribed,
                        subscribeToUpdates,
                        unsubscribeToUpdates);
                    }}
                    color={subscribed ? 'primary' : 'default'}
                  >
                    {subscribed ? 'Listening' : 'Not listening'}
                  </Button>

                  <Select
                    value={chartType}
                    onChange={this.handleChartTypeChange}
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
              <FlowChart
                {...flowChartProps}
                chartType={chartType}
                currentDataPoint={currentDataPoint}
              />
            </Grid>
          </Grid >
        )}
      </DeepstreamSensorProvider>
    );
  }
}

export default withStyles(styles)(RealtimeChart);
