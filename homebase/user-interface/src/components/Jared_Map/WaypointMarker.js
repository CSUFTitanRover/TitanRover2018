/* TODO
Add onClick to select
Add color ability
Add label or ordinal
Make scaling work better with zoom
*/

import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Marker } from 'react-map-gl';
import markerImage from './waypoint.png';

const MIN_SIZE = 16;
const MAX_SIZE = 96;

/** The marker displaying on the react map, showing the coordinate of each waypoint. */
export default class WaypointMarker extends Component {
  render() {
    // The size that the image displays as
    let size = Math.min(Math.max(this.props.zoom * MIN_SIZE / 2, MIN_SIZE), MAX_SIZE);
    if (this.props.selected) { // Grow to show if selected
      size *= 2;
    }

    return (
      <Marker
        latitude={this.props.latitude}
        longitude={this.props.longitude}
        offsetLeft={-size / 2}
        offsetTop={-size}
        captureDrag={false}
      >
        <img src={markerImage} alt="" width={size} height={size} style={{ pointerEvents: 'none' }} />
      </Marker>
    );
  }
}

WaypointMarker.propTypes = {
  zoom: PropTypes.number,
  latitude: PropTypes.number.isRequired,
  longitude: PropTypes.number.isRequired,
  selected: PropTypes.bool,
};

WaypointMarker.defaultProps = {
  zoom: 1,
  selected: false,
};
