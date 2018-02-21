import React, { Component } from 'react';
import PropTypes from 'prop-types';
import List from 'material-ui/List';
import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';

import WaypointModal from './WaypointModal';
import WaypointListItem from './WaypointListItem';

/** The right side of the Map that has the waypoint list and buttons */
export default class WaypointPane extends Component {
  state = {
    modalWaypoint: null,
    modalOpen: false,
  }

  /** Update the modal waypoint data with the received data from WaypointModal */
  _handleModalChange = (event) => {
    this.setState(prevState => ({
      modalWaypoint: { ...prevState.modalWaypoint, [event.target.id]: event.target.value },
    }));
  }

  /** When add is clicked, open the modal */
  _handleAdd = () => {
    this.props.onSelectWaypoint(undefined);
    this.setState({
      modalOpen: true,
      modalWaypoint: undefined,
    });
  }

  /** When edit is clicked, open the modal, passing in that waypoint's data */
  _handleEdit = () => {
    this.setState({
      modalOpen: true,
      modalWaypoint: this.props.selectedWaypoint,
    });
  }

  /** Remove a waypoint from the waypoint list */
  _handleDelete = () => {
    const newWaypoints = [...this.props.waypoints];
    const index = newWaypoints.indexOf(this.props.selectedWaypoint);
    newWaypoints.splice(index, 1);
    this.props.onSelectWaypoint(undefined);
    this.props.onUpdateWaypoints(newWaypoints);
  }

  /** Handle the user closing/submitting the modal */
  _handleClose = (change) => {
    this.setState({
      modalOpen: false,
    });

    // If submit
    if (change) {
      // Convert latitude and longitude to numbers
      const newWaypoints = [...this.props.waypoints];
      const modalWaypoint = this.state.modalWaypoint;
      modalWaypoint.latitude = Number(modalWaypoint.latitude);
      modalWaypoint.longitude = Number(modalWaypoint.longitude);

      // If it was being edited
      if (this.props.selectedWaypoint) {
        // Set the waypoint at that index to the new waypoint data
        const index = newWaypoints.indexOf(this.props.selectedWaypoint);
        if (index >= 0) {
          newWaypoints[index] = this.state.modalWaypoint;
        }
      } else {
        // Otherwise, add the new data to the end
        newWaypoints.push(this.state.modalWaypoint);
      }

      // Update parent state
      this.props.onUpdateWaypoints(newWaypoints);
    }
  }

  /** Handle waypoint selection
  _handleSelectWaypoint = waypoint => () => {
    this.props.onSelectWaypoint(waypoint);
  } */

  render() {
    return (
      <div>
        <Grid
          container
          direction="column"
          className={'MuiPaper-shadow2-5'}
          style={{ width: '340px', padding: '8px', margin: '8px' }}
        >
          <Grid item>
            <List dense disablePadding style={{ height: '320px', maxHeight: '320px', overflow: 'auto', position: 'relative' }}>
              {this.props.waypoints.map(waypoint =>
                (<WaypointListItem
                  key={`waypointlist${waypoint.title}`}
                  onClick={this.props.onSelectWaypoint}
                  waypoint={waypoint}
                  selected={waypoint === this.props.selectedWaypoint}
                />),
              )}
            </List>
          </Grid>

          <Grid item container justify="space-around">
            <Button raised onClick={this._handleAdd}>Add</Button>
            <Button raised disabled={!this.props.selectedWaypoint} onClick={this._handleEdit} color="accent">
              Edit
            </Button>
            <Button raised disabled={!this.props.selectedWaypoint} onClick={this._handleDelete}>
              Delete
            </Button>
          </Grid>
        </Grid>

        <WaypointModal
          onRequestClose={this._handleClose}
          onModalChange={this._handleModalChange}
          open={this.state.modalOpen}
          {...this.state.modalWaypoint}
        />
      </div>
    );
  }
}

WaypointPane.propTypes = {
  waypoints: PropTypes.arrayOf(PropTypes.object),
  selectedWaypoint: PropTypes.object,
  onSelectWaypoint: PropTypes.func.isRequired,
  onUpdateWaypoints: PropTypes.func.isRequired,
};

WaypointPane.defaultProps = {
  waypoints: [],
  selectedWaypoint: undefined,
};

