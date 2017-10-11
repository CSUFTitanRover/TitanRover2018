/* global window */
import React, { Component } from 'react';
import ReactMapGL, { NavigationControl } from 'react-map-gl';
import PropTypes from 'prop-types';
import 'mapbox-gl/dist/mapbox-gl.css';

const navStyle = {
  position: 'absolute',
  top: 0,
  left: 0,
  padding: '10px',
};

export default class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewport: {
        latitude: 37.785164,
        longitude: -100,
        zoom: 1,
        bearing: 0,
        pitch: 0,
        width: 500,
        height: 500,
      },
      popupInfo: null,
    };
  }

  componentDidMount() {
    window.addEventListener('resize', this._resize);
    this._resize();
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this._resize);
  }

  _resize = () => {
    this.setState({
      viewport: {
        ...this.state.viewport,
        width: this.props.width || window.innerWidth,
        height: this.props.height || window.innerHeight,
      },
    });
  };

  _updateViewport = (viewport) => {
    console.log(viewport.latitude);
    this.setState({ viewport });
  }

  render() {
    return (
      <ReactMapGL
        {...this.state.viewport}
        mapStyle="http://localhost:8080/styles/klokantech-basic/style.json"
        onViewportChange={this._updateViewport}
      >


        <div className="nav" style={navStyle}>
          <NavigationControl onViewportChange={this._updateViewport} />
        </div>

      </ReactMapGL>
    );
  }
}

Map.propTypes = {
  width: PropTypes.number,
  height: PropTypes.number,
};

Map.defaultProps = {
  width: 400,
  height: 400,
};
