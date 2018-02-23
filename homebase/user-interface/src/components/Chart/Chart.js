/* eslint-disable */
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
import uuidv4 from 'uuid/v4';
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
    chartName: PropTypes.string,
    yLabel: PropTypes.string,
    chartType: PropTypes.string,
    maxPoints: PropTypes.number,
    chartData: PropTypes.arrayOf(PropTypes.object),
    timestampFormat: PropTypes.string,
    tickFormat: PropTypes.string,
    culling: PropTypes.oneOfType([PropTypes.bool, PropTypes.shape({ max: PropTypes.number })]),
    classes: PropTypes.object.isRequired,
    withDeepstream: PropTypes.bool,
    Toolbar: PropTypes.node,
  }

  static defaultProps = {
    yLabel: 'data',
    chartType: 'line',
    chartData: [],
    maxPoints: 8,
    timestampFormat: '%Y-%m-%dT%H:%M:%S.%LZ',
    tickFormat: '%H:%M:%S',
    culling: false,
    withDeepstream: false,
  };

  renderToolbar = () => {
    const { } = this.props;
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

              <Select value={chartType} onChange={this.handleSelect} className={classes.toolbarItemSpacing}>
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

export default withStyles(styles)(Chart);
