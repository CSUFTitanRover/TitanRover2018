import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import Typography from 'material-ui/Typography';
import { openLeftMenu } from '../../actions/';

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
      display: leftMenuActive ? 'none' : 'flex',
    };

    return (
      <AppBar position="static" className={classNames}>
        <Toolbar>
          <IconButton color="contrast" aria-label="Menu" onClick={handleOnClick} style={iconStyle}>
            <MenuIcon />
          </IconButton>
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
