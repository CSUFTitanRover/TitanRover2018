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
import { closeActionMenu } from '../../actions/menu';
import Poker from '../../components/Poker/';

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

const styles = {
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    padding: '0 10px',
  },
};

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
  };

  static defaultProps = {
    actionMenuActive: false,
    drawerPaperClassNames: '',
  };

  render() {
    const { actionMenuActive, handleOnClick, drawerPaperClassNames } = this.props;

    return (
      <Drawer
        anchor="right"
        open={actionMenuActive}
        classes={{
          paper: drawerPaperClassNames,
        }}
      >
        <div style={styles.drawerHeader}>
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
        </List>
      </Drawer>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(ActionMenu);
