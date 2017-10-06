import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Drawer from 'material-ui/Drawer';
import List from 'material-ui/List';
import Divider from 'material-ui/Divider';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import LayoutMenuList from '../../components/LayoutMenuList/';
import ComponentMenuList from '../../components/ComponentMenuList/';
import { closeLeftMenu } from '../../actions/';

const propTypes = {
  /** handles dispatching the method to close the left menu */
  handleOnClick: PropTypes.func.isRequired,
  /** current active state of left menu */
  leftMenuActive: PropTypes.bool.isRequired,
  /** A string of class names to apply to the LeftMenu for styling concerns. */
  classNames: PropTypes.string.isRequired,
};

const defaultProps = {
  leftMenuActive: false,
  classNames: '',
};

const mapStateToProps = state => ({ leftMenuActive: state.leftMenuActive });

const mapDispatchToProps = dispatch => ({
  handleOnClick: () => {
    dispatch(closeLeftMenu());
  },
});

const styles = {
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 10px',
  },
};

/**
 * The LeftMenu allows quick access to load saved layouts and also select react components
 * that will be added to the Golden-Layout playground.
 */
class LeftMenu extends Component {
  render() {
    const { leftMenuActive, handleOnClick, classNames } = this.props;

    return (
      <Drawer type="persistent" open={leftMenuActive} className={classNames}>
        <div style={styles.drawerHeader}>
          <Typography type="headline">Titan Rover</Typography>
          <IconButton onClick={handleOnClick}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider light />
        <List>
          <LayoutMenuList open={false} />
          <Divider />
          <ComponentMenuList />
        </List>
      </Drawer >
    );
  }
}

LeftMenu.propTypes = propTypes;
LeftMenu.defaultProps = defaultProps;

export default connect(mapStateToProps, mapDispatchToProps)(LeftMenu);
