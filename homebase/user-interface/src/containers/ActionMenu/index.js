import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import { withStyles } from '@material-ui/core/styles';
import { closeActionMenu } from '../../actions/menu';
import Poker from '../../components/Poker/';
import MotorSpeedSwitch from '../../components/MotorSpeedSwitch';
import {
  JOINT_1_ADDRESS,
  JOINT_4_ADDRESS,
  JOINT_51_ADDRESS,
  JOINT_52_ADDRESS,
} from '../../utils/motor_constants';

const mapStateToProps = state => ({ actionMenuActive: state.actionMenuActive });

const mapDispatchToProps = dispatch => ({
  handleOnClick: () => {
    // dispatch the window resize method to force the GL Playground to resize itself
    // this gets rid of the extra spacing that appears
    // although it's kind of a hacky approach
    setTimeout(() => window.dispatchEvent(new Event('resize')), 250);

    dispatch(closeActionMenu());
  },
});

const styles = theme => ({
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    padding: '0 10px',
  },
  motorSubheading: {
    marginTop: theme.spacing.unit * 2,
    marginLeft: theme.spacing.unit * 3,
    color: theme.palette.primary.main,
  },
});

/**
 * The LeftMenu allows quick access to load saved layouts and also select react components
 * that will be added to the Golden-Layout playground.
 */
class ActionMenu extends Component {
  static propTypes = {
    /** handles dispatching the method to close the action menu */
    handleOnClick: PropTypes.func.isRequired,
    /** current active state of left menu */
    actionMenuActive: PropTypes.bool.isRequired,
    /** A string of class names to apply to the LeftMenu for styling concerns. */
    drawerPaperClassNames: PropTypes.string,
    classes: PropTypes.object.isRequired,
  };

  static defaultProps = {
    actionMenuActive: false,
    drawerPaperClassNames: '',
  };

  render() {
    const {
      actionMenuActive,
      handleOnClick,
      drawerPaperClassNames,
      classes,
    } = this.props;

    return (
      <Drawer
        anchor="right"
        open={actionMenuActive}
        classes={{
          paper: drawerPaperClassNames,
        }}
        onClose={handleOnClick}
      >
        <div className={classes.drawerHeader}>
          <Tooltip title="Close Actions" placement="bottom">
            <IconButton aria-label="Close Actions" onClick={handleOnClick} >
              <ChevronRightIcon />
            </IconButton>
          </Tooltip>
          <Typography variant="headline">Quick Actions</Typography>
        </div>
        <Divider light />
        <List>
          <ListItem>
            <Poker />
          </ListItem>
          <Divider light />
          <Typography variant="subheading" className={classes.motorSubheading}>Manage Motor Speeds</Typography>
          <ListItem>
            <MotorSpeedSwitch jointName="Joint 1" address={JOINT_1_ADDRESS} />
          </ListItem>
          <ListItem>
            <MotorSpeedSwitch jointName="Joint 4" address={JOINT_4_ADDRESS} />
          </ListItem>
          <ListItem>
            <MotorSpeedSwitch jointName="Joint 5.1" address={JOINT_51_ADDRESS} />
          </ListItem>
          <ListItem>
            <MotorSpeedSwitch jointName="Joint 5.2" address={JOINT_52_ADDRESS} />
          </ListItem>
        </List>
      </Drawer>
    );
  }
}

const ActionMenuWithStyles = withStyles(styles)(ActionMenu);

export default connect(mapStateToProps, mapDispatchToProps)(ActionMenuWithStyles);
