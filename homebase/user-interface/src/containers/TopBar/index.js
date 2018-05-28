import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import SettingsApplicationsIcon from '@material-ui/icons/SettingsApplications';
import { openLeftMenu, openActionMenu } from '../../actions/menu';
import { DeepstreamStopwatch as Stopwatch } from '../../components/Stopwatch/';

const mapStateToProps = state => ({
  leftMenuActive: state.leftMenuActive,
  actionMenuActive: state.actionMenuActive,
});

const mapDispatchToProps = dispatch => ({
  handleMenuClick: () => {
    // dispatch the window resize method to force the GL Playground to resize itself
    // this gets rid of the extra spacing that appears
    // although it's kind of a hacky approach
    setTimeout(() => window.dispatchEvent(new Event('resize')), 225);

    dispatch(openLeftMenu());
  },

  handleActionsClick: () => {
    // dispatch the window resize method to force the GL Playground to resize itself
    // this gets rid of the extra spacing that appears
    // although it's kind of a hacky approach
    setTimeout(() => window.dispatchEvent(new Event('resize')), 225);

    dispatch(openActionMenu());
  },

});

/**
 * The TopBar renders a menu icon button to open the left menu
 * and will show the Stopwatch component
 */
class TopBar extends Component {
  static propTypes = {
    /** handles dispatching the method to open the left menu */
    handleMenuClick: PropTypes.func.isRequired,
    /** handles dispatching the method to open the actions menu */
    handleActionsClick: PropTypes.func.isRequired,
    /** current active state of left menu */
    leftMenuActive: PropTypes.bool.isRequired,
    /** current active state of actions menu */
    actionMenuActive: PropTypes.bool.isRequired,
    /** A string of class names to apply to the TopBar for styling concerns. */
    classNames: PropTypes.string.isRequired,
  };

  static defaultProps = {
    leftMenuActive: false,
    actionMenuActive: false,
    classNames: '',
  };

  render() {
    const {
      leftMenuActive,
      actionMenuActive,
      handleMenuClick,
      handleActionsClick,
      classNames,
    } = this.props;
    const menuIconStyle = {
      visibility: leftMenuActive ? 'hidden' : 'visible',
    };

    const actionMenuIconStyle = {
      visibility: actionMenuActive ? 'hidden' : 'visible',
    };

    return (
      <AppBar position="static" className={classNames}>
        <Toolbar>
          <Tooltip title="Open Menu" placement="bottom">
            <IconButton color="inherit" aria-label="Open Menu" onClick={handleMenuClick} style={menuIconStyle} >
              <MenuIcon />
            </IconButton>
          </Tooltip>
          <Stopwatch />

          <Tooltip title="Open Actions" placement="bottom">
            <IconButton color="inherit" aria-label="Open Menu" onClick={handleActionsClick} style={actionMenuIconStyle} >
              <SettingsApplicationsIcon />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar >
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(TopBar);
