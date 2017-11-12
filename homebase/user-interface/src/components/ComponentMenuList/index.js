import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Collapse from 'material-ui/transitions/Collapse';
import EqualizerIcon from 'material-ui-icons/Equalizer';
import InboxIcon from 'material-ui-icons/Inbox';
import ExpandLess from 'material-ui-icons/ExpandLess';
import ExpandMore from 'material-ui-icons/ExpandMore';

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

        <Collapse in={this.state.open} transitionDuration="auto">
          <ListItem button className={classes.nested}>
            <ListItemIcon>
              <EqualizerIcon />
            </ListItemIcon>
            <ListItemText inset primary="Sensor #1" />
          </ListItem>
          <ListItem button className={classes.nested}>
            <ListItemIcon>
              <EqualizerIcon />
            </ListItemIcon>
            <ListItemText inset primary="Sensor #2" />
          </ListItem>
          <ListItem button className={classes.nested}>
            <ListItemIcon>
              <EqualizerIcon />
            </ListItemIcon>
            <ListItemText inset primary="Sensor #3" />
          </ListItem>
        </Collapse>
      </List>
    );
  }
}

ComponentMenuList.propTypes = propTypes;

ComponentMenuList.defaultProps = defaultProps;

export default withStyles(styles)(ComponentMenuList);
