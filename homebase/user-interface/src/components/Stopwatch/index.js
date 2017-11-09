import React, { Component } from 'react';
import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';
import { withDeepstreamState } from '../../utils/deepstream';

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
export default class Stopwatch extends Component {
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
    return (
      <Paper style={{ display: 'inline-block', padding: '8px' }}>
        <Grid item container spacing={16} align={'center'}>
          <Grid item style={{ width: '300px', padding: '4px' }}>
            <Typography type="title">Rover Mission Timer</Typography>
          </Grid>
          <Grid item>
            <Paper style={{ width: '200px', padding: '4px' }}><Typography type="subheading">{this.state.time}</Typography>
            </Paper></Grid>
          <Grid item>
            <Button raised color="primary" onClick={this.handleStartAndStop}>
              {this.state.active ? 'Stop' : 'Start'}
            </Button></Grid>
          <Grid item>
            <Button raised color="accent" onClick={this.handleClear}>
              Clear
            </Button></Grid>
        </Grid>
      </Paper>
    );
  }
}

/** This is a class that allows Stopwatch to be synchronized
 *  across all devices connected to deepstream.  The data is stored
 *  under the record 'ui/stopwatch'.
 */
export const DeepstreamStopwatch = withDeepstreamState(Stopwatch, 'ui/stopwatch', ['active', 'startTime', 'accTime']);
