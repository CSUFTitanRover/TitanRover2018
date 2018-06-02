import React, { Component } from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import moment from 'moment';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import green from '@material-ui/core/colors/green';
import red from '@material-ui/core/colors/red';
import grey from '@material-ui/core/colors/grey';
import { withStyles } from '@material-ui/core/styles';
import { getClient } from '../../utils/deepstream';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider';

const styles = theme => ({
  container: {
    display: 'flex',
    alignItems: 'center',
    justifyItems: 'flex-start',
    flex: 1,
  },
  item: {
    marginLeft: theme.spacing.unit * 2,
    marginRight: theme.spacing.unit * 2,
  },
  paper: {
    padding: `${theme.spacing.unit}px ${theme.spacing.unit * 2}px`,
    background: grey[50],
    boxShadow: theme.shadows[3],
    borderRadius: 3,
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
            <Typography
              variant="title"
              color="inherit"
              className={classes.item}
            >
              Mission Stopwatch
            </Typography>
            <div className={cn(classes.paper, classes.item)}>
              <Typography variant="headline" align="center">
                {this.formatTime(elapsedTime)}
              </Typography>
            </div>
            <Button
              variant="raised"
              color="primary"
              className={cn(
                classes.item,
                classes.stopwatchTriggerButton,
                (active ? classes.stopButton : classes.startButton),
              )}
              onClick={this.handleStartAndStop}
            >
              {active ? 'Stop' : 'Start'}
            </Button>
            <Button
              variant="raised"
              color="default"
              onClick={this.handleClear}
              className={classes.item}
            >
              Clear
            </Button>
          </div>
        )}
      </DeepstreamRecordProvider>
    );
  }
}

export default withStyles(styles)(Stopwatch);
