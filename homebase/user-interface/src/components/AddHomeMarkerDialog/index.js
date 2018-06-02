import React, { Component } from 'react';
import PropTypes from 'prop-types';
import has from 'lodash.has';
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

class AddHomeMarkerDialog extends Component {
  static propTypes = {
    isOpen: PropTypes.bool.isRequired,
    handleClose: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
    data: PropTypes.object,
  }

  static defaultProps = {
    data: {
      latitude: 'No latitude found.',
      longitude: 'No longitude found.',
    },
  }

  state = { isAddingWaypoint: false }

  async componentDidMount() {
    this.client = await getClient('homebase');
  }

  handleClose = () => {
    this.props.handleClose();
  }

  handleAddWaypoint = () => {
    const { latitude, longitude } = this.props.data;
    console.log(latitude, longitude);
    this.client.record.setData('homebase/map', { homebaseMarker: { latitude, longitude } });
    this.props.handleClose();
  }

  render() {
    const { isAddingWaypoint } = this.state;
    const { data, isOpen, classes } = this.props;

    const latitude = has(data, 'latitude') ? data.latitude : 'No Latitude Found.';
    const longitude = has(data, 'longitude') ? data.longitude : 'No Longitude Found.';


    return (
      <Dialog open={isOpen} onClose={this.handleClose} aria-labelledby="quick-add-waypoint-dialog">
        <DialogTitle id="quick-add-waypoint-dialog">Are you sure you want to set the home marker?</DialogTitle>
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
            {isAddingWaypoint ? <CircularProgress size={20} color="default" /> : 'Confirm'}
          </Button>
        </DialogActions>
      </Dialog >
    );
  }
}

export default withStyles(styles)(AddHomeMarkerDialog);
