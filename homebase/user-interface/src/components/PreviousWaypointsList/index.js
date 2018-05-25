import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import grey from '@material-ui/core/colors/grey';
import { withStyles } from '@material-ui/core/styles';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';
import WaypointList from '../WaypointList/';

const styles = theme => ({
  container: {
    paddingRight: theme.spacing.unit * 2,
    paddingLeft: theme.spacing.unit * 2,
    background: grey[200],
    height: 'inherit',
    overflow: 'scroll',
  },
  title: {
    marginTop: theme.spacing.unit * 2,
  },
  subheading: {
    display: 'flex',
    marginTop: theme.spacing.unit,
  },
});

class PreviousWaypointsList extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };


  state = {
    data: [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]],
  }

  handleNewPayload = (data) => {
    if (data && data.length > 0) {
      this.setState({ data: data.pp.reverse() });
    }
  }

  renderWaypointList = (data) => {
    const { classes } = this.props;

    if (data.length === 0) {
      return null;
    }
    return (
      <div className={classes.container}>
        <Typography variant="title" className={classes.title}>Previous Waypoints</Typography>
        <WaypointList data={data} waypointListType="previousPoints" />
      </div>
    );
  }

  render() {
    const { data } = this.state;

    return (
      <DeepstreamRecordProvider
        recordPath="rover/currentPoints"
        onNewPayload={this.handleNewPayload}
      >
        {() => this.renderWaypointList(data)}
      </DeepstreamRecordProvider>
    );
  }
}

export default withStyles(styles)(PreviousWaypointsList);
