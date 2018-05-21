import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';
import DeveloperBoardIcon from '@material-ui/icons/DeveloperBoard';
import StarIcon from '@material-ui/icons/Star';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';

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
 * Lists all the saved layouts
 */
class LayoutMenuList extends Component {
  state = { open: this.props.open };

  handleSubmenuClick = () => {
    this.setState(prevState => ({ open: !prevState.open }));
  };

  render() {
    const { classes } = this.props;

    return (
      <List dense>
        <ListItem button onClick={this.handleSubmenuClick} disabled>
          <ListItemIcon>
            <StarIcon />
          </ListItemIcon>
          <ListItemText inset primary="Saved Layouts" />
          {this.state.open ? <ExpandLess /> : <ExpandMore />}
        </ListItem>

        <Collapse in={this.state.open}>
          <ListItem button className={classes.nested}>
            <ListItemIcon>
              <DeveloperBoardIcon />
            </ListItemIcon>
            <ListItemText inset primary="Layout #1" />
          </ListItem>
          <ListItem button className={classes.nested}>
            <ListItemIcon>
              <DeveloperBoardIcon />
            </ListItemIcon>
            <ListItemText inset primary="Layout #2" />
          </ListItem>
          <ListItem button className={classes.nested}>
            <ListItemIcon>
              <DeveloperBoardIcon />
            </ListItemIcon>
            <ListItemText inset primary="Layout #3" />
          </ListItem>
        </Collapse>
      </List>
    );
  }
}

LayoutMenuList.propTypes = propTypes;

LayoutMenuList.defaultProps = defaultProps;

export default withStyles(styles)(LayoutMenuList);
