import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import TextField from '@material-ui/core/TextField';
import green from '@material-ui/core/colors/green';
import grey from '@material-ui/core/colors/grey';
import blueGrey from '@material-ui/core/colors/blueGrey';
import shortid from 'shortid';
import { toast } from 'react-toastify';
import appSettings from '../../appSettings.json';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider';
import { getClient, syncInitialRecordState } from '../../utils/deepstream';

const styles = theme => ({
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

/** The camera settings allows you to change the current IP and protocol
 * the stream is connection to. In addition, you can toggle on or off the
 * camera, save the current image onto the rover, and change the stream quality.
 */
class CameraSettings extends PureComponent {
  static propTypes = {
    /** Property passed in from Material UI withStyles() */
    classes: PropTypes.object.isRequired,
    /** The unique camera ID */
    cameraID: PropTypes.string.isRequired,
    /** The base IP of all camera strings. (e.g. http://192.168.1.173)
     *  Defaults to the option in appSettings.json if no prop is received */
    baseIP: PropTypes.string,
    /** The base port of all camera strings. (e.g. 8080)
     *  Defaults to the option in appSettings.json if no prop is received */
    basePort: PropTypes.string,
    /** Refers to the protocol transport used (e.g. http or https) */
    protocol: PropTypes.oneOf(['http', 'https']),
  }

  static defaultProps = {
    baseIP: appSettings.cameras.baseIP,
    basePort: appSettings.cameras.basePort,
    protocol: 'http',
  }

  generatedSettingID = shortid.generate();
  dsHomebaseClient = null;
  computedRecordPath = `homebase/cameras/${this.props.cameraID}`

  state = {
    streamQuality: 'mid',
    streamIsOffline: true,
    baseIP: this.props.baseIP,
    protocol: this.props.protocol,
  }

  async componentDidMount() {
    const { computedRecordPath } = this;
    this.dsHomebaseClient = await getClient('homebase');

    try {
      // we call the function with the current "this" scope
      // in order to use this.setState correctly
      await syncInitialRecordState.call(this,
        this.dsHomebaseClient,
        computedRecordPath,
        this.state,
      );
    } catch (err) {
      toast.error(err);
    }
  }

  handleStreamQualityChange = async ({ target }) => {
    try {
      const streamQuality = target.value;
      await this._modifyStreamQuality(streamQuality);
      this.dsHomebaseClient.record.setData(this.computedRecordPath, 'streamQuality', streamQuality);
    } catch (err) {
      toast.error(`${err.name}: ${err.message}. Unable to set motion stream quality & maxrate.`);
    }
  }

  _modifyStreamQuality = (quality) => {
    const { basePort, cameraID } = this.props;
    const { baseIP, protocol } = this.state;
    let motionStreamQuality;
    let motionStreamMaxrate;

    switch (quality) {
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
        return Promise.reject('Invalid quality setting provided to modify stream to.');
    }
    return Promise.all([
      fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_quality=${motionStreamQuality}`, { mode: 'no-cors' }),
      fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_maxrate=${motionStreamMaxrate}`, { mode: 'no-cors' }),
    ]);
  }

  handleStreamActivityChange = async () => {
    try {
      const streamIsOffline = !this.state.streamIsOffline;
      await this._toggleStreamActivity(streamIsOffline);
      this.dsHomebaseClient.record.setData(this.computedRecordPath, 'streamIsOffline', streamIsOffline);
    } catch (err) {
      toast.error(`${err.name}: ${err.message}. Unable to modify stream activity.`);
    }
  }

  _toggleStreamActivity = (streamIsOffline) => {
    const { basePort, cameraID } = this.props;
    const { baseIP, protocol } = this.state;

    if (streamIsOffline) {
      // turn the stream on
      const newStreamPort = `${basePort.slice(0, -1)}${cameraID}`;

      return fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_port=${newStreamPort}`, { mode: 'no-cors' });
    }
    // turn the stream off
    return fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/config/set?stream_port=0`, { mode: 'no-cors' });
  }

  handleSaveImage = async () => {
    const { basePort, cameraID } = this.props;
    const { baseIP, protocol } = this.state;
    try {
      await fetch(`${protocol}://${baseIP}:${basePort}/${cameraID}/action/snapshot`, { mode: 'no-cors' });
      toast.info(`Image from Camera #${cameraID} should be saved to /var/lib/motion directory.`);
    } catch (err) {
      toast.error(`${err.name}: ${err.message}. Unable to save image onto rover.`);
    }
  }

  handleBaseIPChange = ({ target }) => {
    const baseIP = target.value;
    this.dsHomebaseClient.record.setData(this.computedRecordPath, 'baseIP', baseIP);
  }

  handleProtocolChange = ({ target }) => {
    const protocol = target.value;
    this.dsHomebaseClient.record.setData(this.computedRecordPath, 'protocol', protocol);
  }

  handleNewPayload = (payload) => { this.setState(payload); }

  render() {
    const { classes } = this.props;
    const { streamQuality, streamIsOffline, baseIP, protocol } = this.state;

    return (
      <DeepstreamRecordProvider
        clientType="homebase"
        recordPath={this.computedRecordPath}
        onNewPayload={this.handleNewPayload}
      >
        {() => (
          <AppBar position="static" color="default" square elevation={1} className={classes.appbar} >
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
                <InputLabel htmlFor={`camera-protocol-${this.generatedSettingID}`}>Stream Protocol</InputLabel>
                <Select
                  value={protocol}
                  onChange={this.handleProtocolChange}
                  inputProps={{
                    id: `camera-protocol-${this.generatedSettingID}`,
                  }}
                >
                  <MenuItem value="http">http</MenuItem>
                  <MenuItem value="https">https</MenuItem>
                </Select>
              </FormControl>
              <FormControl className={classes.formControl}>
                <InputLabel htmlFor={`camera-quality-${this.generatedSettingID}`}>Stream Quality</InputLabel>
                <Select
                  value={streamQuality}
                  onChange={this.handleStreamQualityChange}
                  inputProps={{
                    id: `camera-setting-${this.generatedSettingID}`,
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
                  label={`Stream ${streamIsOffline ? 'Online' : 'Offline'}`}
                  control={
                    <Switch
                      classes={{
                        checked: classes.checked,
                        bar: classes.bar,
                      }}
                      checked={streamIsOffline}
                      onChange={this.handleStreamActivityChange}
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
        )}
      </DeepstreamRecordProvider>
    );
  }
}
export default withStyles(styles)(CameraSettings);
