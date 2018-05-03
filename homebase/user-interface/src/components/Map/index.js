import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactMapGL, { NavigationControl, Marker } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import has from 'lodash.has';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';
import RoverIcon from './RoverIcon';

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
    latitude: 34.8969705992351, // 33.872405,
    longitude: -117.02052467151029, // -117.7748628,
    zoom: 13,
    bearing: 0,
    pitch: 0,
  };

  state = { viewport: this.DEFAULT_VIEWPORT, currentDataPoint: {} }

  _updateViewport = (viewport) => {
    this.setState({ viewport });
  }

  handleMapClick = ({ lngLat }) => {
    const [lng, lat] = lngLat;
    console.log(`Clicked on: lat=${lat} lng=${lng}`);
  }

  renderMap = (currentDataPoint) => {
    const { viewport } = this.state;
    const { width, height, mapStyle } = this.props;
    // const bearing = viewport.bearing;
    // const latitude = viewport.latitude;
    // const longitude = viewport.longitude;

    // if (has(currentDataPoint, 'heading')) {
    //   bearing = currentDataPoint.heading;
    // }

    // if (has(currentDataPoint, 'lat')) {
    //   latitude = currentDataPoint.lat;
    // }

    // if (has(currentDataPoint, 'lon')) {
    //   longitude = currentDataPoint.lon;
    // }

    return (
      <div>
        <ReactMapGL
          {...viewport}
          {...this.mapSettings}
          mapStyle={mapStyle}
          onViewportChange={this._updateViewport}
          width={width}
          height={height}
          // latitude={latitude}
          // longitude={longitude}
          // bearing={bearing}
          onClick={this.handleMapClick}
        >
          <div style={{ position: 'absolute', top: 0, right: 0, padding: 10 }}>
            <NavigationControl onViewportChange={this._updateViewport} />
          </div>

          <RoverIcon
            {...currentDataPoint}
            bearing={viewport.bearing}
            pitch={viewport.pitch}
          />
        </ReactMapGL>
      </div>
    );
  }

  handleNewPayload = (payload) => {
    const { currentDataPoint } = this.state;

    // let's copy the payload and overwrite any keys in currentDataPoint
    // this is done to avoid updating the currentDataPoint without losing any keys
    // that we need
    this.setState({ currentDataPoint: { ...currentDataPoint, ...payload } });
  }

  render() {
    const { currentDataPoint } = this.state;

    return (
      <DeepstreamRecordProvider recordPath={['rover/reach', 'rover/imu']} onNewPayload={this.handleNewPayload}>
        {({ subscribed }) => this.renderMap(currentDataPoint, subscribed)}
      </DeepstreamRecordProvider >
    );
  }
}

export default Map;
