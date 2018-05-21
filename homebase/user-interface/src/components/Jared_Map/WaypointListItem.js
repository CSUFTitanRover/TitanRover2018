import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

import { formatCoordinate } from '../../utils/coordinates';

/** Each element in the list on the WaypointPane */
export default class WaypointListItem extends Component {
  render() {
    const waypoint = this.props.waypoint;

    return (
      <ListItem
        button
        onClick={this.props.onClick(waypoint)}
        style={{
          transition: 'background-color .5s',
          backgroundColor: this.props.selected ? '#fff0f0' : 'transparent',
        }}
      >
        <ListItemText
          primary={waypoint.title}
          secondary={`${formatCoordinate(waypoint.latitude, false)}, \
                        ${formatCoordinate(waypoint.longitude, true)}`}
        />
      </ListItem>
    );
  }
}

WaypointListItem.propTypes = {
  onClick: PropTypes.func.isRequired,
  waypoint: PropTypes.object.isRequired,
  selected: PropTypes.bool.isRequired,
};

