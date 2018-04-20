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
import green from 'material-ui/colors/green';
import grey from 'material-ui/colors/grey';
import uuidv4 from 'uuid/v4';
import appSettings from '../../app-settings.json';

const styles = theme => ({
  root: {
    width: '100%',
  },
  appbar: {
    backgroundColor: '#222',
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
    streamQuality: 'mid',
    streamOnline: true,
  }
  cameraSettingControlsUUID = uuidv4();

  handleSelectChange = ({ target }) => {
    this.setState({ streamQuality: target.value });
    this.modifyVideoStream(target.value);
  }

  modifyVideoStream = (value) => {
    const { baseIP, basePort, cameraID } = this.props;
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

    fetch(`${baseIP}:${basePort}/${cameraID}/config/set?stream_quality=${motionStreamQuality}`, { mode: 'no-cors' });
    fetch(`${baseIP}:${basePort}/${cameraID}/config/set?stream_maxrate=${motionStreamMaxrate}`, { mode: 'no-cors' });
  }

  handleVideoActivityChange = () => {
    this.setState((prevState) => {
      this.toggleVideoStreamActivity(prevState.streamOnline);
      return { streamOnline: !prevState.streamOnline };
    });
  }

  toggleVideoStreamActivity = (streamOnline) => {
    const { baseIP, basePort, cameraID } = this.props;

    if (streamOnline) {
      // turn the stream off
      fetch(`${baseIP}:${basePort}/${cameraID}/config/set?stream_port=0`, { mode: 'no-cors' });
    } else {
      // turn the stream on
      const newStreamPort = `${basePort.slice(0, -1)}${cameraID}`;
      fetch(`${baseIP}:${basePort}/${cameraID}/config/set?stream_port=${newStreamPort}`, { mode: 'no-cors' });
    }
  }

  handleSaveImage = () => {
    const { baseIP, basePort, cameraID } = this.props;
    fetch(`${baseIP}:${basePort}/${cameraID}/action/snapshot`, { mode: 'no-cors' });
    console.info(`Image from Camera #${cameraID} should be saved to /var/lib/motion directory.`);
  }


  render() {
    const { classes, cameraID } = this.props;
    const { streamQuality, streamOnline } = this.state;

    return (
      <div className={classes.root}>
        <AppBar position="static" color="default" className={classes.appbar} square elevation={0}>
          <Toolbar>
            <Typography type="body2" className={classes.cameraLabel}>
              {`Camera #${cameraID} Settings`}
            </Typography>
            <FormControl className={classes.formControl}>
              <InputLabel htmlFor={`camera-quality-${this.cameraSettingControlsUUID}`}>Stream Quality</InputLabel>
              <Select
                value={streamQuality}
                onChange={this.handleSelectChange}
                inputProps={{
                  id: `camera-setting-${this.cameraSettingControlsUUID}`,
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
            <FormControl className={classes.formControl}>
              <Button raised dense color="primary" onClick={this.handleSaveImage}>
                <SaveIcon />
                Save image to rover
              </Button>
            </FormControl>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}
export default withStyles(styles)(CameraSettingControls);
