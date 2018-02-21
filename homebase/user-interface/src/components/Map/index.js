/* TODO:
Use https://react-dnd.github.io/react-dnd/examples-sortable-simple.html
  for changing order of waypoints
Show rover and heading on map and in text
  Allow option in modal to set coordinates as waypoints
*/

import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Paper from 'material-ui/Paper';
import Grid from 'material-ui/Grid';

import 'mapbox-gl/dist/mapbox-gl.css';
import ReactMapGL, { NavigationControl } from 'react-map-gl';

import WaypointMarker from './WaypointMarker';
import WaypointPane from './WaypointPane';

const appSettings = require('../../app-settings.json');

// Test data - remove later
const TEST_WAYPOINTS = [
  { title: 'Waypoint 1', latitude: 47.3769, longitude: 8.5417 },
  { title: 'Waypoint 2', latitude: -34.603722, longitude: -58.381592 },
  { title: 'Waypoint 3', latitude: -54.603722, longitude: -36.381592 },
  { title: 'Waypoint 4', latitude: -32.603722, longitude: -56.381592 },
  { title: 'Waypoint 5', latitude: -89.603722, longitude: -52.381592 },
  { title: 'Waypoint 6', latitude: -23.603722, longitude: -23.381592 },
  { title: 'Waypoint 7', latitude: -56.603722, longitude: -15.381592 },
  { title: 'Waypoint 8', latitude: -75.603722, longitude: -67.381592 },
];


/** Displays a map with waypoints, and a pane that can add, remove, and edit waypoints */
export default class Map extends Component {
  static defaultProps = {
    mapWidth: 400,
    mapHeight: 400,
  };

  static propTypes = {
    mapWidth: PropTypes.number,
    mapHeight: PropTypes.number,
  };

  DEFAULT_VIEWPORT = {
    latitude: 37.785164,
    longitude: -100,
    zoom: 0,
    bearing: 0,
    pitch: 0,
    width: this.props.mapWidth,
    height: this.props.mapHeight,
  };

  state = {
    selectedWaypoint: undefined,
    waypoints: TEST_WAYPOINTS,
    viewport: this.DEFAULT_VIEWPORT,
  };

  /** Change the viewport state */
  _updateViewport = (viewport) => {
    this.setState({ viewport });
  }

  /** Change the waypoint list */
  _updateWaypoints = (waypoints) => {
    this.setState({ waypoints });
  }

  /** Change the selected waypoint */
  _selectWaypoint = (waypoint) => {
    this.setState(prevState => ({
      selectedWaypoint: prevState.selectedWaypoint === waypoint ? undefined : waypoint,
    }));
  }

  render() {
    return (
      <Paper style={{ display: 'inline-block', padding: '8px' }}>
        <Grid container style={{ flexWrap: 'nowrap' }}>
          <Grid item>
            { /* Map object */}
            <ReactMapGL
              {...this.state.viewport}
              mapStyle={appSettings.map.style}
              mapboxApiAccessToken={appSettings.map.mapboxToken}
              onViewportChange={this._updateViewport}
            >
              { /* All the waypoint markers */}
              {this.state.waypoints.map(waypoint =>
                (<WaypointMarker
                  key={`marker${waypoint.title}`}
                  latitude={waypoint.latitude}
                  zoom={this.state.viewport.zoom}
                  longitude={waypoint.longitude}
                  selected={waypoint === this.state.selectedWaypoint}
                />),
              )}

              { /* Navigation bar */}
              <div className="nav" style={{ position: 'absolute', top: 0, left: 0, padding: 10 }}>
                <NavigationControl onViewportChange={this._updateViewport} />
              </div>
            </ReactMapGL>

            { /* Right side pane */}
            <Grid item>
              <WaypointPane
                onSelectWaypoint={this._selectWaypoint}
                onUpdateWaypoints={this._updateWaypoints}
                selectedWaypoint={this.state.selectedWaypoint}
                waypoints={this.state.waypoints}
              />
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}
