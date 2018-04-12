import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Collapse from 'material-ui/transitions/Collapse';
import ShowChartIcon from 'material-ui-icons/ShowChart';
import InboxIcon from 'material-ui-icons/Inbox';
import VideocamIcon from 'material-ui-icons/Videocam';
import ExpandLess from 'material-ui-icons/ExpandLess';
import ExpandMore from 'material-ui-icons/ExpandMore';
import SettingsIcon from 'material-ui-icons/Settings';
import GpsFixedIcon from 'material-ui-icons/GpsFixed';
import NavigationIcon from 'material-ui-icons/Navigation';
import ComponentMenuItem from './ComponentMenuItem';

const propTypes = {
  /** classes is passed down via withStyles() */
  classes: PropTypes.object.isRequired,
  /** Sets the menu list to be open or not */
  open: PropTypes.bool,
};

const defaultProps = {
  open: true,
};

const styles = theme => ({
  nested: {
    paddingLeft: theme.spacing.unit * 4,
  },
});

/**
 * Lists ready-to-use components
 */
class ComponentMenuList extends Component {
  state = { open: this.props.open };

  handleSubmenuClick = () => {
    this.setState(prevState => ({ open: !prevState.open }));
  };

  render() {
    const { classes } = this.props;

    return (
      <List dense>
        <ListItem button onClick={this.handleSubmenuClick}>
          <ListItemIcon>
            <InboxIcon />
          </ListItemIcon>
          <ListItemText inset primary="Components" />
          {this.state.open ? <ExpandLess /> : <ExpandMore />}
        </ListItem>

        <Collapse in={this.state.open}>
          <ComponentMenuItem
            title="Camera #1"
            componentname="Camera"
            icon={<VideocamIcon />}
            className={classes.nested}
            componentprops={{ cameraID: '1' }}
          />
          <ComponentMenuItem
            title="Camera #2"
            componentname="Camera"
            icon={<VideocamIcon />}
            className={classes.nested}
            componentprops={{ cameraID: '2' }}
          />
          <ComponentMenuItem
            title="Camera #3"
            componentname="Camera"
            icon={<VideocamIcon />}
            className={classes.nested}
            componentprops={{ cameraID: '3' }}
          />
          <ComponentMenuItem
            title="Camera #4"
            componentname="Camera"
            icon={<VideocamIcon />}
            className={classes.nested}
            componentprops={{ cameraID: '4' }}
          />
          <ComponentMenuItem
            title="Decagon Realtime Chart"
            componentname="RealtimeChart"
            icon={<ShowChartIcon />}
            className={classes.nested}
            componentprops={{ chartName: 'Decagon-5TE', subscriptionPath: 'science/decagon' }}
          />
          <ComponentMenuItem
            title="Altimeter Realtime Chart"
            componentname="RealtimeChart"
            icon={<ShowChartIcon />}
            className={classes.nested}
            componentprops={{ chartName: 'Altimeter', subscriptionPath: 'science/altimeter' }}
          />
          <ComponentMenuItem
            title="DHT Realtime Chart"
            componentname="RealtimeChart"
            icon={<ShowChartIcon />}
            className={classes.nested}
            componentprops={{ chartName: 'DHT', subscriptionPath: 'science/dht' }}
          />
          <ComponentMenuItem
            title="Atmospheric Realtime Chart"
            componentname="RealtimeChart"
            icon={<ShowChartIcon />}
            className={classes.nested}
            componentprops={{ chartName: 'Atmospheric', subscriptionPath: 'science/atmospheric' }}
          />
          <ComponentMenuItem
            title="Rover API Settings"
            componentname="RoverApiSettings"
            icon={<SettingsIcon />}
            className={classes.nested}
          />
          <ComponentMenuItem
            title="Start Autonomy"
            componentname="StartAutonomyButton"
            icon={<GpsFixedIcon />}
            className={classes.nested}
          />
          <ComponentMenuItem
            title="Map"
            componentname="ResizeAwareMap"
            icon={<NavigationIcon />}
            className={classes.nested}
          />
        </Collapse>
      </List>
    );
  }
}

ComponentMenuList.propTypes = propTypes;

ComponentMenuList.defaultProps = defaultProps;

export default withStyles(styles)(ComponentMenuList);
