import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText, ListSubheader } from 'material-ui/List';
import Typography from 'material-ui/Typography';
import { toast } from 'react-toastify';
import Divider from 'material-ui/Divider';
import { InputLabel } from 'material-ui/Input';
import { FormControl } from 'material-ui/Form';
import { MenuItem } from 'material-ui/Menu';
import Button from 'material-ui/Button';
import Select from 'material-ui/Select';
import ClearIcon from 'material-ui-icons/Clear';
import PowerIcon from 'material-ui-icons/PowerSettingsNew';
import RestoreIcon from 'material-ui-icons/SettingsBackupRestore';
import SyncIcon from 'material-ui-icons/Sync';
import appSettings from '../../appSettings.json';

// taken from /rover/core/process-manager/processses.json
// CRA does not allow imports from outside the /src folder
const screenNames = [
  {
    screenName: 'motion',
  },
  {
    screenName: 'mobility',
  },
  {
    screenName: 'speed',
  },
  {
    screenName: 'reach',
  },
  {
    screenName: 'reachSocketServer',
  },
  {
    screenName: 'autonomanual',
  },
  {
    screenName: 'roverAPI',
  },
];

const { roverAPI } = appSettings;
const { base_ip, base_port } = roverAPI;

const styles = theme => ({
  root: {
    width: '100%',
    backgroundColor: theme.palette.background.paper,
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
    maxWidth: 300,
  },
  restartScreenButton: {
    margin: theme.spacing.unit,
  },
  restartScreenContainer: {
    padding: theme.spacing.unit,
    minWidth: 400,
  },
});

class RoverApiSettings extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  }

  state = { screenName: '' }

  fetchRoverAPI = async (apiName) => {
    try {
      let response = await fetch(`//${base_ip}:${base_port}${apiName}`);
      response = response.json();
      if (response.status === 'SUCCESS') {
        toast.success(`${apiName} request succeeded!`);
      } else {
        throw new Error('Request failed.');
      }
    } catch (err) {
      toast.error(`${err.name}: ${err.message} [${apiName}]`);
      console.error(err);
    }
  }

  restartScreen = () => {
    const { screenName } = this.state;

    if (screenName.length <= 0) {
      toast.error('No screen name selected to restart.');
      return;
    }

    const apiName = `/restartScreen/${screenName}`;
    this.fetchRoverAPI(apiName);
  }

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <List component="nav" subheader={<ListSubheader component="div">Rover Api Settings</ListSubheader>}>
          <ListItem button onClick={() => { this.fetchRoverAPI('/clearLogFiles'); }}>
            <ListItemIcon>
              <ClearIcon />
            </ListItemIcon>
            <ListItemText primary="Clear Log Files" />
          </ListItem>
          <ListItem button onClick={() => { this.fetchRoverAPI('/restartTheRover'); }}>
            <ListItemIcon>
              <RestoreIcon />
            </ListItemIcon>
            <ListItemText primary="Restart Rover" />
          </ListItem>
          <ListItem button onClick={() => { this.fetchRoverAPI('/shutdownTheRover'); }}>
            <ListItemIcon>
              <PowerIcon />
            </ListItemIcon>
            <ListItemText primary="Shutdown Rover" />
          </ListItem>
          <ListItem button onClick={() => { this.fetchRoverAPI('/syncMotion'); }}>
            <ListItemIcon>
              <SyncIcon />
            </ListItemIcon>
            <ListItemText primary="Sync Motion" />
          </ListItem>
        </List>
        <Divider />

        <div className={classes.restartScreenContainer}>
          <Typography variant="title">
            Restart Screen Session
          </Typography>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="screenNames">Screen Name</InputLabel>
            <Select
              value={this.state.screenName}
              onChange={({ target: { value } }) => this.setState({ screenName: value })}
              inputProps={{
                name: 'screenNames',
                id: 'screenNames',
              }}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {screenNames.map(({ screenName }) => (
                <MenuItem value={screenName} key={screenName}>
                  {screenName}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button variant="raised" color="primary" onClick={this.restartScreen}>
            Restart Session
          </Button>
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(RoverApiSettings);
