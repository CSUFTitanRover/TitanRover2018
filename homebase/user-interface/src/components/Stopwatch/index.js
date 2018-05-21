import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import green from '@material-ui/core/colors/green';
import red from '@material-ui/core/colors/red';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import { withDeepstreamState } from '../../utils/deepstream';

const styles = theme => ({
  paper: {
    padding: '4px',
  },
  stopwatchTriggerButton: {
    transition: theme.transitions.create(['background'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  startButton: {
    background: green[500],
    '&:hover': {
      background: green[700],
    },
  },
  stopButton: {
    background: red[500],
    '&:hover': {
      background: red[700],
    },
  },
});

/** Adds leading zeros to a number, plus an ending character */
const padZeros = (number, length, ending) => (`${number}`).padStart(length, '0') + ending;

/** Formats a duration in milliseconds to a time string */
const formatTime = (elapsed) => {
  // Find total elapsed time and separate it into its components
  let ms = elapsed;
  let sec = Math.floor(ms / 1000);
  ms %= 1000;
  let min = Math.floor(sec / 60);
  sec %= 60;
  const hour = Math.floor(min / 60);
  min %= 60;

  return padZeros(hour, 2, ':') + padZeros(min, 2, ':') + padZeros(sec, 2, '.') + padZeros(ms, 3, '');
};

/**
 * Stopwatch component
 * Keeps track of elapsed mission time.
 */
class Stopwatch extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  }

  /**
   * state:
   *  time: displayed time value (string)
   *  active: whether it is running (boolean)
   *  startTime: when the time was last started/resumed (int)
   *  accTime: how much time has accumulated (int)
   */
  state = { time: '00:00:00.000', active: false, startTime: 0, accTime: 0 }

  componentDidMount() {
    window.requestAnimationFrame(this.tick);
  }

  /** Update the display time value */
  tick = () => {
    window.requestAnimationFrame(this.tick);

    // Get current ms running
    let ms = (new Date()).getTime();
    if (!this.state.active) {
      ms = 0;
    }

    // Find total elapsed time and update time string
    const elapsed = ms - this.state.startTime + this.state.accTime;
    this.setState({
      time: formatTime(elapsed),
    });
  }

  /** Activate/deactivate the timer when the start/stop button is pressed */
  handleStartAndStop = () => {
    this.setState((prevState) => {
      // Timer is stopped
      let newStartTime = (new Date()).getTime();
      let newAccTime = prevState.accTime;

      if (prevState.active) {
        // Find out the elapsed time on the timer and stop the interval
        newAccTime = (new Date()).getTime() - prevState.startTime + prevState.accTime;
        newStartTime = 0;
      }

      // Toggle active state
      return { active: !prevState.active, startTime: newStartTime, accTime: newAccTime };
    });
  };

  /** Clears all states */
  handleClear = () => {
    this.setState({
      active: false,
      startTime: 0,
      accTime: 0,
    });
  }

  render() {
    const { classes } = this.props;
    const { active } = this.state;
    return (
      <Grid container spacing={16} alignItems="center">
        <Grid item xs={2}>
          <Typography variant="title" color="inherit">Mission Stopwatch</Typography>
        </Grid>
        <Grid item xs={2}>
          <Paper className={classes.paper}>
            <Typography>{this.state.time}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={1}>
          <Button variant="raised" color="primary" className={classNames(classes.stopwatchTriggerButton, (active ? classes.stopButton : classes.startButton))} onClick={this.handleStartAndStop}>
            {this.state.active ? 'Stop' : 'Start'}
          </Button>
        </Grid>
        <Grid item xs={1}>
          <Button variant="raised" color="default" onClick={this.handleClear}>
            Clear
          </Button>
        </Grid>
      </Grid>
    );
  }
}

const StopwatchWithStyles = withStyles(styles)(Stopwatch);
export default StopwatchWithStyles;

/** This is a class that allows Stopwatch to be synchronized
 *  across all devices connected to deepstream.  The data is stored
 *  under the record 'ui/stopwatch'.
 */
export const DeepstreamStopwatch = withDeepstreamState(StopwatchWithStyles, 'ui/stopwatch', ['active', 'startTime', 'accTime']);
