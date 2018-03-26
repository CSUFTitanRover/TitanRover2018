import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-map-gl';
import RoverDirectionIcon from '../../resources/rover-direction-icon.svg';

// svg icon width and height
const svgWidth = 50;
const svgHeight = 50;

// find the offset's to center the icon
const offsetLeft = (svgWidth / 2) * -1;
const offsetTop = (svgHeight / 2) * -1;

class RoverIcon extends PureComponent {
  static propTypes = {
    lat: PropTypes.number,
    lon: PropTypes.number,
    heading: PropTypes.number,
    bearing: PropTypes.number.isRequired,
  }

  static defaultProps = {
    lat: 0,
    lon: 0,
    heading: 0,
  }

  render() {
    const { lat, lon, heading, bearing } = this.props;

    const roverIconStyles = {
      outline: '2px solid red',
      transformOrigin: 'center',
      transform: `rotate(${heading - bearing}deg)`,
    };

    return (
      <Marker
        latitude={lat}
        longitude={lon}
        offsetLeft={offsetLeft}
        offsetTop={offsetTop}
      >
        <div style={roverIconStyles}>
          <img src={RoverDirectionIcon} alt="rover direction icon" width={svgWidth} height={svgHeight} />
        </div>
      </Marker>
    );
  }
}

export default RoverIcon;
