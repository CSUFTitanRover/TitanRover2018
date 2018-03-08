import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import SaveIcon from 'material-ui-icons/Save';
import Select from 'material-ui/Select';
import { MenuItem } from 'material-ui/Menu';
import { InputLabel } from 'material-ui/Input';
import { FormControl, FormControlLabel } from 'material-ui/Form';
import Switch from 'material-ui/Switch';
import TextField from 'material-ui/TextField';
import green from 'material-ui/colors/green';
import grey from 'material-ui/colors/grey';
import blueGrey from 'material-ui/colors/blueGrey';
import shortid from 'shortid';
import appSettings from '../../appSettings.json';
import DeepstreamRecordProvider from '../../containers/DeepstreamRecordProvider';
import { getClient } from '../../utils/deepstream';

window.ds = null;

const styles = theme => ({
  root: {
    width: '100%',
  },
  appbar: {
    backgroundColor: blueGrey[100],
  },
  cameraLabel: {
    color: grey[200],
    paddingRight: 10,
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 110,
  },
  bar: {},
  checked: {
    color: green[500],
    '& + $bar': {
      backgroundColor: green[500],
    },
  },
});

class CameraSettingControls extends PureComponent {
  static propTypes = {
    /** Property passed in from Material UI withStyles */
    classes: PropTypes.object.isRequired,
    /** The unique camera ID */
    cameraID: PropTypes.string.isRequired,
    /** The base IP of all camera strings. (e.g. http::/localhost)
     *  Defaults to the option in appSettings.json if no prop is received */
    baseIP: PropTypes.string,
    /** The base port of all camera strings. (e.g. 8080)
     *  Defaults to the option in appSettings.json if no prop is received */
    basePort: PropTypes.string,
    /** Refers to the protocol transport used (e.g. http or https) */
    protocol: PropTypes.string,
    /** Handles changing the base IP of the camera stream source in the Camera Component */
    cameraWrapperBaseIPChange: PropTypes.func.isRequired,
  }

  static defaultProps = {
    baseIP: appSettings.cameras.base_ip,
    basePort: appSettings.cameras.base_port,
    protocol: 'http',
  }

  cameraSettingControlsID = shortid.generate();
  dsHomebaseClient = null;
  computedRecordPath = `homebase/cameras/${this.props.cameraID}`

  state = {
    streamQuality: 'mid',
    streamOnline: true,
    baseIP: this.props.baseIP,
    protocol: this.props.protocol,
  }

  async componentDidMount() {
    const { computedRecordPath } = this;
    this.dsHomebaseClient = await getClient('homebase');

    // initialize ds state to match up with our initial
    // component state if the record does not already exist
    this.dsHomebaseClient.record.has(computedRecordPath, (error, hasRecord) => {
      if (!hasRecord) {
        this.dsHomebaseClient.record.setData(computedRecordPath, this.state);
      }
    });
  }

  handleSelectChange = ({ target }) => {
    const state = { streamQuality: target.value };
    this.setState(state);
    this.dsHomebaseClient.record.setData(this.computedRecordPath, state);
    this.modifyVideoStream(target.value);
  }

  modifyVideoStream = (value) => {
    const { basePort, cameraID } = this.props;
    const { baseIP, protocol } = this.state;
    let motionStreamQuality;
    let motionStreamMaxrate;

    switch (value) {
      case 'low':
        motionStreamQuality = 4;
        motionStreamMaxrate = 4;
        break;

      case 'mid':
        motionStreamQuality = 20;
        motionStreamMaxrate = 10;
        break;

      case 'high':
        motionStreamQuality = 50;
        motionStreamMaxrate = 20;
        break;

      case 'ultra':
        motionStreamQuality = 75;
        motionStreamMaxrate = 30;
        break;
      default:
        break;
    }

    fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_quality=${motionStreamQuality}`, { mode: 'no-cors' });
    fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_maxrate=${motionStreamMaxrate}`, { mode: 'no-cors' });
  }

  handleVideoActivityChange = () => {
    this.setState((prevState) => {
      const state = { streamOnline: !prevState.streamOnline };
      this.toggleVideoStreamActivity(prevState.streamOnline);
      this.dsHomebaseClient.record.setData(this.computedRecordPath, { streamOnline: !prevState.streamOnline });
      return state;
    });
  }

  toggleVideoStreamActivity = (streamOnline) => {
    const { basePort, cameraID } = this.props;
    const { baseIP, protocol } = this.state;

    if (streamOnline) {
      // turn the stream off
      fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_port=0`, { mode: 'no-cors' });
    } else {
      // turn the stream on
      const newStreamPort = `${basePort.slice(0, -1)}${cameraID}`;
      fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_port=${newStreamPort}`, { mode: 'no-cors' });
    }
  }

  handleSaveImage = () => {
    const { basePort, cameraID } = this.props;
    const { baseIP, protocol } = this.state;
    fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/action/snapshot`, { mode: 'no-cors' });
    console.info(`Image from Camera #${cameraID} should be saved to /var/lib/motion directory.`);
  }

  handleBaseIPChange = ({ target }) => {
    const state = { baseIP: target.value };
    this.dsHomebaseClient.record.setData(this.computedRecordPath, state);
    this.setState(state);
    this.props.cameraWrapperBaseIPChange(target.value);
  }

  handleProtocolChange = ({ target }) => {
    const state = { protocol: target.value };
    this.dsHomebaseClient.record.setData(this.computedRecordPath, state);
    this.setState(state);
  }

  handleNewPayload = (payload) => { this.setState(payload); }

  render() {
    const { classes } = this.props;
    const { streamQuality, streamOnline, baseIP, protocol } = this.state;

    return (
      <DeepstreamRecordProvider
        clientType="homebase"
        recordPath={this.computedRecordPath}
        onNewPayload={this.handleNewPayload}
      >
        {() => (
          <div className={classes.root}>
            <AppBar position="static" className={classes.appbar} square elevation={0}>
              <Toolbar>
                <Typography variant="body2">
                  Camera Settings
                </Typography>
                <TextField
                  id="baseIP"
                  label="Base IP"
                  value={baseIP}
                  onChange={this.handleBaseIPChange}
                  className={classes.formControl}
                />
                <FormControl className={classes.formControl}>
                  <InputLabel htmlFor={`camera-protocol-${this.cameraSettingControlsID}`}>Stream Protocol</InputLabel>
                  <Select
                    value={protocol}
                    onChange={this.handleProtocolChange}
                    inputProps={{
                      id: `camera-protocol-${this.cameraSettingControlsID}`,
                    }}
                  >
                    <MenuItem value="http">http</MenuItem>
                    <MenuItem value="https">https</MenuItem>
                  </Select>
                </FormControl>
                <FormControl className={classes.formControl}>
                  <InputLabel htmlFor={`camera-quality-${this.cameraSettingControlsID}`}>Stream Quality</InputLabel>
                  <Select
                    value={streamQuality}
                    onChange={this.handleSelectChange}
                    inputProps={{
                      id: `camera-setting-${this.cameraSettingControlsID}`,
                    }}
                  >
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="mid">Mid</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="ultra">Ultra</MenuItem>
                  </Select>
                </FormControl>
                <FormControl className={classes.formControl}>
                  <FormControlLabel
                    label={`Stream ${streamOnline ? 'Online' : 'Offline'}`}
                    control={
                      <Switch
                        classes={{
                          checked: classes.checked,
                          bar: classes.bar,
                        }}
                        checked={streamOnline}
                        onChange={this.handleVideoActivityChange}
                        aria-label="Stream Activity Switch"
                      />}
                  />
                </FormControl>
                <Button variant="raised" size="small" color="primary" onClick={this.handleSaveImage}>
                  <SaveIcon />
                  Save image to rover
                </Button>
              </Toolbar>
            </AppBar>
          </div>
        )}
      </DeepstreamRecordProvider>
    );
  }
}
export default withStyles(styles)(CameraSettingControls);
