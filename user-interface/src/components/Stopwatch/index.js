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

/**
 * Stopwatch component 
 * Keeps track of elapsed mission time.
 */
export default class Stopwatch extends Component {
  constructor(props) {
    super(props);

    /*    time: the display string
          startLabel: the label for the start button
          startTime: when the time was last resumed/started
          accTime: the time accumulated before the timer was paused
          intervalId: the interval driving the stopwatch
    */
    this.state = { time: 'some time value', startLabel: 'Start', startTime: this.props.s || 0, accTime: 0, intervalId: null };
    this.formatTime(); // TODO: format the time 
  }

  // TODO: Clear interval on unmount!
  formatTime() {
    // Create a function to add leading zeros
    function pad(number, length, ending) {
      return ("0000" + number).slice(-length) + ending;
    }

    // Get current ms running
    var ms = (new Date()).getTime();
    if (this.state.startTime === 0) { // Not currently running
      ms = 0;
    }

    // Find total elapsed time and separate it into its components
    var elapsed = ms - this.state.startTime + this.state.accTime;
    var sec = Math.floor(elapsed / 1000);
    elapsed %= 1000;
    var min = Math.floor(sec / 60);
    sec %= 60;
    var hour = Math.floor(min / 60);
    min %= 60;

    // Update the time string
    this.setState({
      time: pad(hour, 2, ":") + pad(min, 2, ":") + pad(sec, 2, ".") + pad(elapsed, 3, "")
    });
  }

  handleStart() {
    if (this.state.startTime === 0) { // Timer is stopped
      // Change label to pause, and set current countdown to the time now
      // Also, start the timer using setInterval
      this.setState({
        startLabel: 'Pause',
        startTime: (new Date()).getTime(),
        intervalId: setInterval(this.formatTime.bind(this), 17)
      });
    } else {
      // Find out the elapsed time on the timer
      var elapsed = (new Date()).getTime() - this.state.startTime + this.state.accTime;

      // Stop the timer
      clearInterval(this.state.intervalId);

      // Change label to start, and reset the start time
      this.setState({
        startLabel: 'Start',
        startTime: 0,
        accTime: elapsed,
        intervalId: null
      });
    }

    this.formatTime();
  };

  handleClear() {
    // Reset all states
    clearInterval(this.state.intervalId);

    this.setState({
      startLabel: 'Start',
      accTime: 0,
      startTime: 0,
      intervalId: null
    }, this.formatTime);
  }

  render() {
    return (
      <Grid container>
        <Paper style={{ padding: "16px" }}>
          <Grid item container spacing={16} align={'center'} lg={6}>
            <Grid item style={{ width: "300px", padding: "4px" }}>
              <Typography type="title">Rover Mission Timer</Typography>
            </Grid>
            <Grid item>
              <Paper style={{ width: "200px", padding: "4px" }}><Typography type="subheading">{this.state.time}</Typography>
              </Paper></Grid>
            <Grid item>
              <Button raised color="primary" onClick={() => this.handleStart()}>
                {this.state.startLabel}
              </Button></Grid>
            <Grid item>
              <Button raised color="accent" onClick={() => this.handleClear()}>
                Clear
              </Button></Grid>
          </Grid>
        </Paper>
      </Grid>
    )
  }
}