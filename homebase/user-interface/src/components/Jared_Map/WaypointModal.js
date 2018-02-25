import React, { Component } from 'react';
import PropTypes from 'prop-types';

import Dialog, { DialogTitle, DialogContent, DialogContentText, DialogActions } from 'material-ui/Dialog';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';

export default class WaypointModal extends Component {
  state = {
    submitEnabled: false,
    /* Status:
      0: unchecked
      1: error
      2: passing
    */
    status: { title: 0, latitude: 0, longitude: 0 },
  };

  // TODO: Refactor this function
  componentWillReceiveProps(newProps) {
    // If the modal is being opened
    if (!this.props.open && newProps.open) {
      const newStatus = newProps.title === '' ? 0 : 2;

      this.setState({
        status: { title: newStatus, latitude: newStatus, longitude: newStatus },
        submitEnabled: newProps.title !== '',
      });
    }
  }

  _handleChange = (event) => {
    // Update the modalWaypoint object in the parent component
    event.persist();
    this.props.onModalChange(event);

    // Check to see that the changed value is valid
    this.setState((prevState) => {
      // TODO: Add function that validates better
      const newStatus = { ...prevState.status, [event.target.id]: event.target.value ? 2 : 1 };

      // Only enable submit if all fields are validated
      return ({
        status: newStatus,
        submitEnabled: Object.values(newStatus).every(key => key === 2),
      });
    });
  }

  _handleSubmit = () => {
    this.props.onRequestClose(true);
  }

  _handleCancel = () => {
    this.props.onRequestClose(false);

    // Reset the state
    this.setState({
      submitEnabled: false,
      status: { title: 0, latitude: 0, longitude: 0 },
    });
  }

  render() {
    return (
      <Dialog onRequestClose={this._handleCancel} open={this.props.open}>
        <DialogTitle>Enter coordinates</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please input the waypoint name, latitude, and longitude (as numbers)
          </DialogContentText>

          { /* All different fields for input */}
          <TextField
            fullWidth
            error={this.state.status.title === 1}
            id="title"
            label="Waypoint name"
            value={this.props.title}
            onChange={this._handleChange}
            style={{ margin: '8px' }}
          />
          <TextField
            error={this.state.status.latitude === 1}
            type="number"
            id="latitude"
            label="Latitude"
            value={this.props.latitude}
            onChange={this._handleChange}
            style={{ margin: '8px' }}
          />
          <TextField
            error={this.state.status.longitude === 1}
            type="number"
            id="longitude"
            label="Longitude"
            value={this.props.longitude}
            onChange={this._handleChange}
            style={{ margin: '8px' }}
          />
        </DialogContent>

        { /* Buttons on the bottom of modal */}
        <DialogActions>
          <Button onClick={this._handleCancel}>Cancel</Button>
          <Button disabled={!this.state.submitEnabled} color="primary" onClick={this._handleSubmit}>Submit</Button>
        </DialogActions>
      </Dialog>
    );
  }
}

WaypointModal.propTypes = {
  onRequestClose: PropTypes.func.isRequired,
  onModalChange: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  title: PropTypes.string,
  latitude: PropTypes.any,
  longitude: PropTypes.any,
};

WaypointModal.defaultProps = {
  title: '',
  latitude: '',
  longitude: '',
};
