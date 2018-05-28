import 'mapbox-gl/dist/mapbox-gl.css';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import has from 'lodash.has';
import cn from 'classnames';
import shortid from 'shortid';
import ReactMapGL, { NavigationControl, Marker, Popup } from 'react-map-gl';
import { withStyles } from '@material-ui/core/styles';
import amber from '@material-ui/core/colors/amber';
import grey from '@material-ui/core/colors/grey';
import MarkerIcon from '@material-ui/icons/LocationOn';
import BreadcrumbIcon from '@material-ui/icons/Lens';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';
import RoverIcon from './RoverIcon';
import QuickAddWaypointDialog from '../QuickAddWaypointDialog/';

const styles = theme => ({
  markerIcon: {
    width: 44,
    height: 44,
    color: theme.palette.primary.main,
  },
  markerIconActive: {
    color: amber[700],
  },
  popupContent: {
    padding: theme.spacing.unit,
    paddingBottom: 0,
    fontFamily: 'Roboto',
    lineHeight: '28px',
  },
  breadcrumbIcon: {
    width: 10,
    height: 10,
    color: grey[800],
  },
});

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
    classes: PropTypes.object.isRequired,
    /** The count of updates at which it gets applied. */
    currentGPSUpdateCountTarget: PropTypes.number,
  }

  static defaultProps = {
    width: 500,
    height: 500,
    currentGPSUpdateCountTarget: 5,
    /** Free vector tile service via https://www.tilehosting.com/ */
    mapStyle: 'https://free.tilehosting.com/styles/basic/style.json?key=rheiM2CFkgsezyxOhNrX',
  }

  mapSettings = {
    touchRotate: true,
  }

  DEFAULT_VIEWPORT = {
    latitude: 33.881932, // 33.872405,
    longitude: -117.882843, // -117.7748628,
    zoom: 15,
    bearing: 0,
    pitch: 0,
  };

  state = {
    viewport: this.DEFAULT_VIEWPORT,
    data: {
      currentGPS: [],
      pp: [],
      cp: [],
      breadcrumbs: [],
    },
    popupInfo: null,
    quickAddDialogOpen: false,
  }

  currentGPSUpdateCountDelayed = 0;

  _updateViewport = (viewport) => {
    this.setState({ viewport });
  }

  handleMapClick = (event) => {
    const [longitude, latitude] = event.lngLat;
    const withCtrlKey = event.srcEvent.ctrlKey;
    const leftButtonClick = event.leftButton;
    const quickAddTriggered = leftButtonClick && withCtrlKey;

    // //console.log(event);
    // console.log(`Clicked on: lat=${latitude} lng=${longitude}`);
    // console.log('CTRL pressed during left click:', quickAddTriggered);

    if (quickAddTriggered) {
      this.setState({ quickAddDialogOpen: true, quickAddLatitude: latitude, quickAddLongitude: longitude });
    }
  }

  renderPopup = () => {
    const { popupInfo } = this.state;
    const { classes } = this.props;

    return popupInfo && (
      <Popup
        anchor="bottom"
        longitude={popupInfo.longitude}
        latitude={popupInfo.latitude}
        onClose={() => this.setState({ popupInfo: null })}
      >
        <div className={classes.popupContent}>
          <div>
            <strong>Latitude:</strong>
            <span>{` ${popupInfo.latitude} `}</span>
          </div>
          <div>
            <strong>Longitude:</strong>
            <span>{` ${popupInfo.longitude}`}</span>
          </div>
        </div>
      </Popup>
    );
  }

  renderMarkers = (data) => {
    const { classes } = this.props;

    if (data && has(data, 'cp')) {
      return (
        data.cp.map(([latitude, longitude], index) => {
          const parsedLatitude = parseFloat(latitude);
          const parsedLongitude = parseFloat(longitude);

          return (
            <Marker
              key={shortid.generate()}
              latitude={parsedLatitude}
              longitude={parsedLongitude}
              offsetLeft={-22}
            >
              <MarkerIcon
                className={cn(
                  classes.markerIcon,
                  { [classes.markerIconActive]: (index === 0) },
                )}
                onClick={() => this.setState({
                  popupInfo: { latitude: parsedLatitude, longitude: parsedLongitude },
                })}
              />
            </Marker>
          );
        })
      );
    }

    return null;
  }

  renderBreadcrumbs = (data) => {
    const { classes } = this.props;

    // should be breadcrumbs instead of pp
    if (data && has(data, 'breadcrumbs')) {
      return (
        data.breadcrumbs.map(([latitude, longitude]) => {
          const parsedLatitude = parseFloat(latitude);
          const parsedLongitude = parseFloat(longitude);

          return (
            <Marker
              key={shortid.generate()}
              latitude={parsedLatitude}
              longitude={parsedLongitude}
              offsetLeft={-5}
            >
              <BreadcrumbIcon className={classes.breadcrumbIcon} />
            </Marker>
          );
        })
      );
    }

    return null;
  }
  closeQuickAddWaypointDialog = () => {
    this.setState({ quickAddDialogOpen: false, quickAddData: null });
  }
  renderMap = () => {
    const {
      viewport,
      data,
      quickAddDialogOpen,
      quickAddLatitude,
      quickAddLongitude,
    } = this.state;
    const { width, height, mapStyle } = this.props;
    // const bearing = viewport.bearing;
    // const latitude = viewport.latitude;
    // const longitude = viewport.longitude;

    let roverLatitude = 0;
    let roverLongitude = 0;
    let roverHeading = 0;

    if (has(data, 'currentGPS')) {
      roverLatitude = data.currentGPS[0];
      roverLongitude = data.currentGPS[1];
    }

    if (has(data, 'heading')) {
      roverHeading = data.heading;
    }

    return (
      <div>
        <QuickAddWaypointDialog
          isOpen={quickAddDialogOpen}
          handleClose={this.closeQuickAddWaypointDialog}
          latitude={quickAddLatitude}
          longitude={quickAddLongitude}
        />
        <ReactMapGL
          {...viewport}
          {...this.mapSettings}
          mapStyle={mapStyle}
          onViewportChange={this._updateViewport}
          width={width}
          height={height}
          onClick={this.handleMapClick}
        >
          <div style={{ position: 'absolute', top: 0, right: 0, padding: 10 }}>
            <NavigationControl onViewportChange={this._updateViewport} />
          </div>

          {this.renderMarkers(data)}
          {this.renderBreadcrumbs(data)}
          {this.renderPopup()}

          <RoverIcon
            latitude={roverLatitude}
            longitude={roverLongitude}
            bearing={viewport.bearing}
            heading={roverHeading}
            pitch={viewport.pitch}
          />
        </ReactMapGL>
      </div>
    );
  }

  handleNewPayload = (payload, recordPath) => {
    const { data } = this.state;
    const { currentGPSUpdateCountTarget } = this.props;
    // console.log(recordPath);
    // console.log(payload);

    // custom logic for currentGPS since it's
    // only an array that gets updated in place [lat, lon]
    if (recordPath === 'rover/currentGPS') {
      const transformedPayload = [payload.latitude, payload.longitude];
      // always add the new payload to the currentGPS
      data.currentGPS = transformedPayload;

      // this.setState(prevState => ({ data: {...prevState.data, currentGPS:  }  }))

      if (this.currentGPSUpdateCountDelayed === currentGPSUpdateCountTarget) {
        data.breadcrumbs = [...data.breadcrumbs, transformedPayload];
        this.currentGPSUpdateCountDelayed = 0;
      } else {
        this.currentGPSUpdateCountDelayed += 1;
      }
      // finally set the new state
      this.setState({ data });
    } else {
      // let's copy the payload and overwrite any keys in currentDataPoint
      // this is done to avoid updating the currentDataPoint without losing any keys
      // that we need
      this.setState({ data: { ...data, ...payload } });
    }
  }

  render() {
    return (
      <DeepstreamRecordProvider
        recordPath={[
          'rover/currentPoints',
          'rover/previousPoints',
          'rover/currentGPS',
          'rover/imu']}
        onNewPayload={this.handleNewPayload}
      >
        {() => this.renderMap()}
      </DeepstreamRecordProvider >
    );
  }
}

export default withStyles(styles)(Map);
