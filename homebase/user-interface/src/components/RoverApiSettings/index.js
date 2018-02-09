import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import appSettings from '../../app-settings.json';
import List, { ListItem, ListItemIcon, ListItemText, ListSubheader } from 'material-ui/List';
import Divider from 'material-ui/Divider';
import InboxIcon from 'material-ui-icons/Inbox';
import DraftsIcon from 'material-ui-icons/Drafts';

const { roverAPI } = appSettings;
const { base_ip, base_port } = roverAPI;

const styles = theme => ({
  root: {
    width: '100%',
    backgroundColor: theme.palette.background.paper,
  },
});

class RoverApiSettings extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  }

  fetchAPI = async (apiName) => {
    try {
      let response = await fetch(`//${base_ip}:${base_port}${apiName}`);
      response = response.json();
      if (response.status === 'SUCCESS') {
        console.log('request succeeded');
      }
    } catch (err) {
      console.error(err);
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <List component="nav" subheader={<ListSubheader component="div">Rover Api Settings</ListSubheader>}>
          <ListItem button onClick={() => { this.fetchAPI('/clearLogFiles'); }}>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary="Clear Log Files" />
          </ListItem>
          <ListItem button onClick={() => { this.fetchAPI('/restartTheRover'); }}>
            <ListItemIcon>
              <DraftsIcon />
            </ListItemIcon>
            <ListItemText primary="Restart Rover" />
          </ListItem>
          <ListItem button onClick={() => { this.fetchAPI('/shutdownTheRover'); }}>
            <ListItemIcon>
              <DraftsIcon />
            </ListItemIcon>
            <ListItemText primary="Shutdown Rover" />
          </ListItem>
          <ListItem button onClick={() => { this.fetchAPI('/syncMotion'); }}>
            <ListItemIcon>
              <DraftsIcon />
            </ListItemIcon>
            <ListItemText primary="Sync Motion" />
          </ListItem>
        </List>
      </div>
    );
  }
}

export default withStyles(styles)(RoverApiSettings);
