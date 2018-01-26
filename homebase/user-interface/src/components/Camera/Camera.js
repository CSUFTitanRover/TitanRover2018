import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import Resizable from 'react-resizable-box';
import { ContextMenu, MenuItem, ContextMenuTrigger } from 'react-contextmenu';
import CheckIcon from 'material-ui-icons/Check';
import uuidv4 from 'uuid/v4';
import appSettings from '../../app-settings.json';
import './styles.css';

const resizableStyles = {
  background: 'lightgray',
};

const fullscreenImageStyles = {
  height: '-webkit-fill-available',
};

class Camera extends PureComponent {
  static propTypes = {
    /** The unique camera ID */
    cameraID: PropTypes.string.isRequired,
    /** The base IP of all camera strings. (e.g. http::/localhost)
     *  Defaults to the option in app-settings.json if no prop is received */
    baseIP: PropTypes.string,
    /** The base port of all camera strings. (e.g. 8080)
     *  Defaults to the option in app-settings.json if no prop is received */
    basePort: PropTypes.string,
  }

  static defaultProps = {
    baseIP: appSettings.cameras.base_ip,
    basePort: appSettings.cameras.base_port,
  }

  state = {
    width: 300,
    height: 300,
    resizing: false,
    savedWidth: null,
    savedHeight: null,
    fullsize: false,
  };

  cameraUUID = uuidv4();

  handleOnResizeStart = () => {
    this.setState({ resizing: true });
  }

  handleOnResizeStop = (e, direction, ref, d) => {
    const { width, height } = this.state;
    this.setState({
      width: width + d.width,
      height: height + d.height,
      resizing: false,
    });
  }

  handleToggleFullSize = () => {
    const { fullsize } = this.state;
    if (fullsize) {
      this.setState(prevState => ({
        fullsize: !prevState.fullsize,
        width: prevState.savedWidth,
        height: prevState.savedHeight,
      }));
    } else {
      this.setState(prevState => ({
        fullsize: !prevState.fullsize,
        savedWidth: prevState.width,
        savedHeight: prevState.height,
        width: '100%',
        height: '100%',
      }));
    }
  }

  render() {
    const { baseIP, basePort, cameraID } = this.props;
    const { width, height, resizing, fullsize } = this.state;
    const computedPort = `${basePort.slice(0, -1)}${cameraID}`;
    return (
      <React.Fragment>
        <ContextMenuTrigger id={`camera-${this.cameraUUID}`} ref={(node) => { this.node = node; }}>
          <Resizable
            style={{
              ...resizableStyles,
              outline: resizing && '3px solid red',
            }}
            width={width}
            height={height}
            onResizeStart={this.handleOnResizeStart}
            onResizeStop={this.handleOnResizeStop}
          >
            <img src={`${baseIP}:${computedPort}`} alt="camera" width={width} height={height} style={fullsize ? fullscreenImageStyles : null} />
          </Resizable>
        </ContextMenuTrigger>

        <ContextMenu id={`camera-${this.cameraUUID}`}>
          <MenuItem onClick={this.handleToggleFullSize}>
            Toggle Fullsize
            {fullsize && <CheckIcon />}
          </MenuItem>
          <MenuItem divider />
          <MenuItem>
            Save Image to Rover
          </MenuItem>
        </ContextMenu>
      </React.Fragment>
    );
  }
}

export default Camera;
