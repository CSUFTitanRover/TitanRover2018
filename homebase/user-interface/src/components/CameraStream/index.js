import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import Resizable from 're-resizable';
import { ContextMenu, MenuItem as ContextMenuItem, ContextMenuTrigger } from 'react-contextmenu';
import shortid from 'shortid';
import ResizeAware from 'react-resize-aware';
import { MenuItem, MenuList } from 'material-ui/Menu';
import { ListItemIcon, ListItemText } from 'material-ui/List';
import Paper from 'material-ui/Paper';
import FullscreenIcon from 'material-ui-icons/Fullscreen';
import FullscreenExitIcon from 'material-ui-icons/FullscreenExit';
import LockIcon from 'material-ui-icons/LockOutline';
import LockOpenIcon from 'material-ui-icons/LockOpen';
import appSettings from '../../app-settings.json';

const resizableStyles = {
  background: 'lightgray',
};

const aspectRatio = 4 / 3;

const enableResizeHandles = {
  top: true,
  right: true,
  bottom: true,
  left: true,
  topRight: true,
  bottomRight: true,
  bottomLeft: true,
  topLeft: true,
};

const disableResizeHandles = {
  top: false,
  right: false,
  bottom: false,
  left: false,
  topRight: false,
  bottomRight: false,
  bottomLeft: false,
  topLeft: false,
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
    /** Refers to the protocol transport used (e.g. http or https) */
    protocol: PropTypes.string,
  }

  static defaultProps = {
    baseIP: appSettings.cameras.base_ip,
    basePort: appSettings.cameras.base_port,
    protocol: 'http',
  }

  generatedID = shortid.generate();
  state = {
    resizableSize: {
      width: 250, // 640,
      height: 250, // 480,
    },
    savedWidth: null,
    savedHeight: null,
    resizeAwareWidth: null,
    resizeAwareHeight: null,
    resizing: false,
    fullsize: false,
    lockAspectRatio: false,
  };

  handleOnResizeStart = () => {
    this.setState({ resizing: true });
  }

  handleOnResizeStop = (e, direction, ref, delta) => {
    const { width, height } = this.state.resizableSize;

    this.setState({
      resizableSize: {
        width: width + delta.width,
        height: height + delta.height,
      },
      resizing: false,
    });
  }

  handleToggleFullSize = () => {
    const { fullsize } = this.state;
    if (fullsize) {
      // turn off full size
      this.setState(prevState => ({
        fullsize: !prevState.fullsize,
      }));
    } else {
      // turn on full size
      this.setState(prevState => ({
        fullsize: !prevState.fullsize,
        lockAspectRatio: false,
      }));
    }
  }

  handleLockRatio = () => {
    this.setState(prevState => ({ lockAspectRatio: !prevState.lockAspectRatio }));
  }

  handleResizeAwareChange = ({ width, height }) => {
    this.setState({
      resizeAwareSize: { width, height },
    });
  }

  render() {
    const { baseIP, basePort, cameraID, protocol } = this.props;
    const { resizableSize, resizing, fullsize, lockAspectRatio, resizeAwareSize } = this.state;
    const computedPort = `${basePort.slice(0, -1)}${cameraID}`;

    return (
      <React.Fragment>
        <ContextMenuTrigger
          id={`camera-${this.generatedID}`}
          attributes={{
            style: { width: 'inherit', height: 'inherit' },
          }}
        >
          <ResizeAware
            onResize={this.handleResizeAwareChange}
            style={{ position: 'relative', width: 'inherit', height: 'inherit' }}
          >

            <Resizable
              style={{
                ...resizableStyles,
                outline: resizing && '3px solid red',
              }}
              size={fullsize ? resizeAwareSize : resizableSize}
              onResizeStart={this.handleOnResizeStart}
              onResizeStop={this.handleOnResizeStop}
              lockAspectRatio={lockAspectRatio && aspectRatio}
              enable={fullsize ? disableResizeHandles : enableResizeHandles}
            >

              <img
                src={`${protocol}://${baseIP}:${computedPort}`}
                alt="camera stream"
                width="100%"
                height="100%"
              />
            </Resizable>
          </ResizeAware>
        </ContextMenuTrigger>

        <ContextMenu id={`camera-${this.generatedID}`}>
          <Paper elevation={12}>
            <MenuList>
              <ContextMenuItem >
                <MenuItem onClick={this.handleToggleFullSize}>
                  <ListItemIcon >
                    {fullsize ? <FullscreenExitIcon /> : <FullscreenIcon />}
                  </ListItemIcon>
                  <ListItemText inset primary={fullsize ? 'Deactivate Fullsize' : 'Activate Fullsize'} />
                </MenuItem>
              </ContextMenuItem>

              <ContextMenuItem disabled={fullsize}>
                <MenuItem onClick={this.handleLockRatio} disabled={fullsize}>
                  <ListItemIcon >
                    {lockAspectRatio ? <LockOpenIcon /> : <LockIcon />}
                  </ListItemIcon>
                  <ListItemText
                    primary={lockAspectRatio ? 'Unlock Aspect Ratio' : 'Lock Aspect Ratio'}
                    secondary="Locks to (4:3)"
                  />
                </MenuItem>
              </ContextMenuItem>
            </MenuList>
          </Paper>
        </ContextMenu>
      </React.Fragment>
    );
  }
}

export default Camera;
