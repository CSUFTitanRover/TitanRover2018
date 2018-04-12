import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import Resizable from 'react-resizable-box';
import { ContextMenu, MenuItem, ContextMenuTrigger } from 'react-contextmenu';
import CheckIcon from 'material-ui-icons/Check';
import shortid from 'shortid';
import appSettings from '../../app-settings.json';
import './styles.css';

const resizableStyles = {
  background: 'lightgray',
};

const aspectRatio = 4 / 3;

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
    /** Refers to the protocol transport used (e.g. http or https) */
    protocol: PropTypes.string,
  }

  static defaultProps = {
    baseIP: appSettings.cameras.base_ip,
    basePort: appSettings.cameras.base_port,
    protocol: 'http',
  }

  state = {
    width: 640,
    height: 480,
    resizing: false,
    savedWidth: null,
    savedHeight: null,
    fullsize: false,
    lockAspectRatio: false,
  };

  cameraID = shortid.generate();

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

  handleLockRatio = () => {
    this.setState(prevState => ({ lockAspectRatio: !prevState.lockAspectRatio }));
  }

  render() {
    const { baseIP, basePort, cameraID, protocol } = this.props;
    const { width, height, resizing, fullsize, lockAspectRatio } = this.state;
    const computedPort = `${basePort.slice(0, -1)}${cameraID}`;
    return (
      <React.Fragment>
        <ContextMenuTrigger id={`camera-${this.cameraID}`} ref={(node) => { this.node = node; }} style={{ width: 'inherit', height: 'inherit' }}>
          <Resizable
            style={{
              ...resizableStyles,
              outline: resizing && '3px solid red',
            }}
            width={width}
            height={height}
            onResizeStart={this.handleOnResizeStart}
            onResizeStop={this.handleOnResizeStop}
            lockAspectRatio={lockAspectRatio && aspectRatio}
          >
            <img src={`${protocol}://${baseIP}:${computedPort}`} alt="camera stream" width="100%" className="camera-stream" />
          </Resizable>
        </ContextMenuTrigger>

        <ContextMenu id={`camera-${this.cameraID}`}>
          <MenuItem onClick={this.handleToggleFullSize}>
            Toggle Fullsize
            {fullsize && <CheckIcon />}
          </MenuItem>
          <MenuItem divider />
          <MenuItem onClick={this.handleLockRatio}>
            Lock aspect ratio to (4:3)
            {lockAspectRatio && <CheckIcon />}
          </MenuItem>
        </ContextMenu>
      </React.Fragment>
    );
  }
}

export default Camera;
