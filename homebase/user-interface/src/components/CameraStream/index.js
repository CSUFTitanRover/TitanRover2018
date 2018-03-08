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
import grey from 'material-ui/colors/grey';
import { toast } from 'react-toastify';
import appSettings from '../../appSettings.json';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider';
import { getClient, syncInitialRecordState } from '../../utils/deepstream';

const resizableStyles = {
  backgroundColor: grey[100],
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


/** The camera stream shows a specified cameras view. It's able to be resized and take up the
 * components full size via the right click menu. You can also lock the aspect ratio if need be
 * to (4:3). In addition, the CameraStream is wired up to deepstream to reflect changes made in
 * the corresponding CameraSettings.
 */
class CameraStream extends PureComponent {
  static propTypes = {
    /** The unique camera ID */
    cameraID: PropTypes.string.isRequired,
  }

  computedRecordPath = `homebase/cameras/${this.props.cameraID}`
  generatedID = shortid.generate();
  state = {
    resizeAwareSize: null,
    resizableSize: {
      width: 400, // 640,
      height: 300, // 480,
    },
    resizing: false,
    fullsize: false,
    lockAspectRatio: false,
    basePort: appSettings.cameras.basePort,
    // this below state is hooked up to deepstream
    baseIP: appSettings.cameras.baseIP,
    protocol: 'http',
  };

  async componentDidMount() {
    const { computedRecordPath } = this;
    this.dsHomebaseClient = await getClient('homebase');
    try {
      const { baseIP, protocol } = this.state;
      const initialState = { baseIP, protocol };

      // we call the function with the current "this" scope
      // in order to use this.setState correctly
      await syncInitialRecordState.call(this,
        this.dsHomebaseClient,
        computedRecordPath,
        initialState,
      );
    } catch (err) {
      toast.error(err);
    }
  }

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

  handleNewPayload = (payload) => { this.setState(payload); }

  render() {
    const { cameraID } = this.props;
    const {
      basePort,
      baseIP,
      protocol,
      resizableSize,
      resizing,
      fullsize,
      lockAspectRatio,
      resizeAwareSize,
    } = this.state;
    const computedPort = `${basePort.slice(0, -1)}${cameraID}`;

    return (
      <DeepstreamRecordProvider
        clientType="homebase"
        recordPath={this.computedRecordPath}
        onNewPayload={this.handleNewPayload}
      >
        {() => (
          <React.Fragment>
            <ContextMenuTrigger
              id={`camera-${this.generatedID}`}
              attributes={{
                style: { width: 'inherit', height: 'inherit' },
              }}
              holdToDisplay={-1}
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
        )}
      </DeepstreamRecordProvider>
    );
  }
}

export default CameraStream;
