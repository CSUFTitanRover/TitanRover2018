import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactMapGL, { NavigationControl } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import has from 'lodash.has';
import { DeepstreamRecordProvider } from '../../utils/deepstream';

/** An offline map that is hooked up into Deepstream to
 * listen for IMU, Reach, and Waypoints record updates.
 */
class Map extends Component {
  static propTypes = {
    /** The width of the map. */
    width: PropTypes.number,
    /** The height of the map. */
    height: PropTypes.number,
    /** The map tile styles that are used. */
    mapStyle: PropTypes.string,
  }

  static defaultProps = {
    width: 500,
    height: 500,
    /** Free vector tile service via https://www.tilehosting.com/ */
    mapStyle: 'https://free.tilehosting.com/styles/basic/style.json?key=rheiM2CFkgsezyxOhNrX',
  }

  mapSettings = {
    touchRotate: true,
  }

  DEFAULT_VIEWPORT = {
    latitude: 33.872405,
    longitude: -117.7748628,
    zoom: 13,
    bearing: 0,
    pitch: 0,
  };

  state = { viewport: this.DEFAULT_VIEWPORT }

  _updateViewport = (viewport) => {
    this.setState({ viewport });
  }

  renderMap = (currentDataPoint) => {
    const { viewport } = this.state;
    const { width, height, mapStyle } = this.props;
    let bearing = viewport.bearing;
    let latitude = viewport.latitude;
    let longitude = viewport.longitude;

    if (has(currentDataPoint, 'heading')) {
      bearing = currentDataPoint.heading;
    }

    if (has(currentDataPoint, 'lat')) {
      latitude = currentDataPoint.lat;
    }

    if (has(currentDataPoint, 'lon')) {
      longitude = currentDataPoint.lon;
    }

    return (
      <div>
        <ReactMapGL
          {...viewport}
          {...this.mapSettings}
          mapStyle={mapStyle}
          onViewportChange={this._updateViewport}
          width={width}
          height={height}
          latitude={latitude}
          longitude={longitude}
          bearing={bearing}
        >

          <div style={{ position: 'absolute', top: 0, right: 0, padding: 10 }}>
            <NavigationControl onViewportChange={this._updateViewport} />
          </div>
        </ReactMapGL>
      </div>
    );
  }

  render() {
    return (
      <DeepstreamRecordProvider recordPath={['rover/reach', 'rover/imu']} >
        {(currentDataPoint, subscribed) => this.renderMap(currentDataPoint, subscribed)}
      </DeepstreamRecordProvider >
    );
  }
}

export default Map;
