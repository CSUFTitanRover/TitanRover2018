import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Tooltip from 'material-ui/Tooltip';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import Typography from 'material-ui/Typography';
import { openLeftMenu } from '../../actions/menu';

const propTypes = {
  /** handles dispatching the method to open the left menu */
  handleOnClick: PropTypes.func.isRequired,
  /** current active state of left menu */
  leftMenuActive: PropTypes.bool.isRequired,
  /** A string of class names to apply to the TopBar for styling concerns. */
  classNames: PropTypes.string.isRequired,
};

const defaultProps = {
  leftMenuActive: false,
  classNames: '',
};

const mapStateToProps = state => ({ leftMenuActive: state.leftMenuActive });

const mapDispatchToProps = dispatch => ({
  handleOnClick: () => {
    // dispatch the window resize method to force the GL Playground to resize itself
    // this gets rid of the extra spacing that appears
    // although it's kind of a hacky approach
    setTimeout(() => window.dispatchEvent(new Event('resize')), 225);

    dispatch(openLeftMenu());
  },
});

/**
 * The TopBar renders a menu icon button to open the left menu
 * and will show the Stopwatch component
 */
class TopBar extends Component {
  render() {
    const { leftMenuActive, handleOnClick, classNames } = this.props;
    const iconStyle = {
      visibility: leftMenuActive ? 'hidden' : 'visible',
    };

    return (
      <AppBar position="static" className={classNames}>
        <Toolbar>
          <Tooltip title="Open Menu" placement="bottom">
            <IconButton color="inherit" aria-label="Open Menu" onClick={handleOnClick} style={iconStyle} >
              <MenuIcon />
            </IconButton>
          </Tooltip>
          <Typography type="title" color="inherit" >
            Mission Elapsed Time
          </Typography>
        </Toolbar>
      </AppBar >
    );
  }
}

TopBar.propTypes = propTypes;
TopBar.defaultProps = defaultProps;

export default connect(mapStateToProps, mapDispatchToProps)(TopBar);
