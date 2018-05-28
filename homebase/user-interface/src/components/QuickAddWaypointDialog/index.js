import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';
import { withStyles } from '@material-ui/core/styles';
import { toast } from 'react-toastify';
import { getClient } from '../../utils/deepstream';

const styles = () => ({
  content: {
    fontFamily: 'Roboto',
  },
});

class QuickAddWaypointDialog extends Component {
  static propTypes = {
    isOpen: PropTypes.bool.isRequired,
    latitude: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    longitude: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    handleClose: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  }

  static defaultProps = {
    latitude: 'No latitude found.',
    longitude: 'No longitude found.',
  }

  state = { isAddingWaypoint: false }

  async componentDidMount() {
    this.client = await getClient();
  }

  handleClose = () => {
    this.props.handleClose();
  }

  handleAddWaypoint = () => {
    const { latitude, longitude } = this.state;
    const computedDataString = `${latitude},${longitude}`;
    this.setState({ isAddingWaypoint: true });

    this.client.rpc.make('addCoordinate', computedDataString, (rpcError, result) => {
      this.setState({ isAddingWaypoint: false });
      if (rpcError) {
        toast.error(rpcError);
      } else {
        toast.success(result);
        this.handleClose();
      }
    });
  }

  render() {
    const { isAddingWaypoint } = this.state;
    const { latitude, longitude, isOpen, classes } = this.props;

    return (
      <Dialog open={isOpen} onClose={this.handleClose} aria-labelledby="quick-add-waypoint-dialog">
        <DialogTitle id="quick-add-waypoint-dialog">Are you sure you want to quick add this waypoint?</DialogTitle>
        <DialogContent>
          <div className={classes.content}>
            <strong>Latitude:</strong>
            <span>{` ${latitude}, `}</span>
            <strong>Longitude:</strong>
            <span>{` ${longitude}`}</span>
          </div>
        </DialogContent>
        <DialogActions>
          <Button onClick={this.handleClose}>Cancel</Button>
          <Button color="primary" variant="raised" onClick={this.handleAddWaypoint}>
            {isAddingWaypoint ? <CircularProgress size={20} color="default" /> : 'Add Waypoint'}
          </Button>
        </DialogActions>
      </Dialog >
    );
  }
}

export default withStyles(styles)(QuickAddWaypointDialog);
