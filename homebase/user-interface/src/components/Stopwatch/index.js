import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import green from '@material-ui/core/colors/green';
import red from '@material-ui/core/colors/red';
import moment from 'moment';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import cn from 'classnames';
import { getClient } from '../../utils/deepstream';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider';

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

/**
 * Stopwatch component
 * Keeps track of elapsed mission time.
 */
class Stopwatch extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  }

  state = { elapsedTime: 0, active: false }

  async componentDidMount() {
    this.client = await getClient('homebase');
  }

  formatTime = value => moment().hour(0).minute(0).second(value)
    .format('HH:mm:ss');

  handleStartAndStop = () => {
    const { active } = this.state;

    if (active) {
      // we want to stop the stopwatch
      this.client.event.emit('homebase/stopwatch:stop');
    } else {
      // we want to start the stopwatch
      this.client.event.emit('homebase/stopwatch:start');
    }
  }

  handleClear = () => {
    this.client.event.emit('homebase/stopwatch:clear');
  }

  handleNewPayload = (data) => {
    this.setState(data);
  }

  render() {
    const { classes } = this.props;
    const { active, elapsedTime } = this.state;

    return (
      <DeepstreamRecordProvider recordPath="homebase/stopwatch" onNewPayload={this.handleNewPayload}>
        {() => (
          <div className={classes.container}>
            <Typography variant="title" color="inherit">Mission Stopwatch</Typography>
            <div className={classes.paper}>
              <Typography>{this.formatTime(elapsedTime)}</Typography>
            </div>
            <Button
              variant="raised"
              color="primary"
              className={cn(classes.stopwatchTriggerButton, (active ? classes.stopButton : classes.startButton))}
              onClick={this.handleStartAndStop}
            >
              {active ? 'Stop' : 'Start'}
            </Button>
            <Button variant="raised" color="default" onClick={this.handleClear}>
              Clear
            </Button>
          </div>
        )}
      </DeepstreamRecordProvider>
    );
  }
}

export default withStyles(styles)(Stopwatch);
