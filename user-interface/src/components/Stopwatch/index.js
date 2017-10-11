/* TODO:
clear interval on unmount
change interval to requestAnimationFrame?
fix spacing and style
*/

import React, { Component } from 'react';
import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

// Adds leading zeros to a number
const pad = (number, length, ending) => (`0000${number}`).slice(-length) + ending;

/**
 * Stopwatch component 
 * Keeps track of elapsed mission time.
 */
export default class Stopwatch extends Component {
  /**
   * state:
   *  time: displayed time value (string)
   *  active: whether it is running (boolean)
   * startTime: when the time was last started/resumed (int)
   * accTime: how much time has accumulated (int)
   * intervalId: the interval updating the time
   */
  state = { time: '00:00:00.000', active: false }
  startTime = 0
  accTime = 0
  intervalId = null

  // Updates the display
  formatTime = () => {
    // Get current ms running
    let ms = (new Date()).getTime();
    if (!this.state.active) { // Not currently running
      ms = 0;
    }

    // Find total elapsed time and separate it into its components
    let elapsed = ms - this.startTime + this.accTime;
    let sec = Math.floor(elapsed / 1000);
    elapsed %= 1000;
    let min = Math.floor(sec / 60);
    sec %= 60;
    const hour = Math.floor(min / 60);
    min %= 60;

    // Update the time string
    this.setState({
      time: pad(hour, 2, ':') + pad(min, 2, ':') + pad(sec, 2, '.') + pad(elapsed, 3, ''),
    });
  }

  // Activate/deactivate the timer when start is pressed
  handleStart = () => {
    // Timer is stopped
    if (!this.state.active) {
      // Set current countdown to the time now and start the timer
      this.startTime = (new Date()).getTime();
      this.intervalId = setInterval(this.formatTime, 17);
    } else {
      // Find out the elapsed time on the timer and stop the interval
      this.accTime = (new Date()).getTime() - this.startTime + this.accTime;
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.startTime = 0;
    }

    // Toggle active
    this.setState({
      active: !this.state.active,
    }, this.formatTime);
  };

  // Clear all states
  handleClear = () => {
    clearInterval(this.intervalId);
    this.intervalId = null;
    this.accTime = 0;
    this.startTime = 0;

    this.setState({
      active: false,
    }, this.formatTime);
  }

  render() {
    return (
      <Grid item container spacing={16} align={'center'} className={'MuiPaper-shadow2-5'} lg={6}>
        <Grid item style={{ width: '300px', padding: '4px' }}>
          <Typography type="title">Rover Mission Timer</Typography>
        </Grid>
        <Grid item>
          <Paper style={{ width: '200px', padding: '4px' }}><Typography type="subheading">{this.state.time}</Typography>
          </Paper></Grid>
        <Grid item>
          <Button raised color="primary" onClick={this.handleStart}>
            {this.state.active ? 'Stop' : 'Start'}
          </Button></Grid>
        <Grid item>
          <Button raised color="accent" onClick={this.handleClear}>
            Clear
          </Button></Grid>
      </Grid>
    );
  }
}
