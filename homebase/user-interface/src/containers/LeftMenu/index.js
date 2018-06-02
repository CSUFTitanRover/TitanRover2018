import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import LayoutMenuList from '../../components/LayoutMenuList/';
import ComponentMenuList from '../../components/ComponentMenuList/';
import { closeLeftMenu } from '../../actions/menu';

// const propTypes = {
//   /** handles dispatching the method to close the left menu */
//   handleOnClick: PropTypes.func.isRequired,
//   /** current active state of left menu */
//   leftMenuActive: PropTypes.bool.isRequired,
//   /** A string of class names to apply to the LeftMenu for styling concerns. */
//   drawerPaperClassNames: PropTypes.string,
// };

// const defaultProps = {
//   leftMenuActive: false,
//   drawerPaperClassNames: '',
// };

// const mapStateToProps = state => ({ leftMenuActive: state.leftMenuActive });

// const mapDispatchToProps = dispatch => ({
//   handleOnClick: () => {
//     // dispatch the window resize method to force the GL Playground to resize itself
//     // this gets rid of the extra spacing that appears
//     // although it's kind of a hacky approach
//     setTimeout(() => window.dispatchEvent(new Event('resize')), 250);

//     dispatch(closeLeftMenu());
//   },
// });

// const styles = {
//   drawerHeader: {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'flex-end',
//     padding: '0 10px',
//   },
// };

// /**
//  * The LeftMenu allows quick access to load saved layouts and also select react components
//  * that will be added to the Golden-Layout playground.
//  */
// class LeftMenu extends Component {
//   render() {
//     const { leftMenuActive, handleOnClick, drawerPaperClassNames } = this.props;

//     return (
//       <Drawer
//         variant="persistent"
//         open={leftMenuActive}
//         classes={{
//           paper: drawerPaperClassNames,
//         }}
//       >
//         <div style={styles.drawerHeader}>
//           <Typography variant="headline">Titan Rover</Typography>
//           <Tooltip title="Close Menu" placement="bottom">
//             <IconButton aria-label="Close Menu" onClick={handleOnClick} >
//               <ChevronLeftIcon />
//             </IconButton>
//           </Tooltip>
//         </div>
//         <Divider light />
//         <List>
//           <LayoutMenuList open={false} />
//           <Divider />
//           <ComponentMenuList />
//         </List>
//       </Drawer>
//     );
//   }
// }

// LeftMenu.propTypes = propTypes;
// LeftMenu.defaultProps = defaultProps;

// export default connect(mapStateToProps, mapDispatchToProps)(LeftMenu);


const propTypes = {
  /** A string of class names to apply to the LeftMenu for styling concerns. */
  drawerPaperClassNames: PropTypes.string,
};

const defaultProps = {
  leftMenuActive: false,
  drawerPaperClassNames: '',
};

const mapStateToProps = state => ({ leftMenuActive: state.leftMenuActive });

const mapDispatchToProps = dispatch => ({
  handleOnClick: () => {
    // dispatch the window resize method to force the GL Playground to resize itself
    // this gets rid of the extra spacing that appears
    // although it's kind of a hacky approach
    setTimeout(() => window.dispatchEvent(new Event('resize')), 250);

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
    const { drawerPaperClassNames } = this.props;

    return (
      <Drawer
        variant="persistent"
        open
        classes={{
          paper: drawerPaperClassNames,
        }}
      >
        <div style={styles.drawerHeader}>
          <Typography variant="headline">Titan Rover</Typography>
          <Tooltip title="Close Menu" placement="bottom">
            <IconButton aria-label="Close Menu" >
              <ChevronLeftIcon />
            </IconButton>
          </Tooltip>
        </div>
        <Divider light />
        {/* <List>
          <LayoutMenuList open={false} />
          <Divider />
          <ComponentMenuList />
        </List> */}
      </Drawer>
    );
  }
}

LeftMenu.propTypes = propTypes;
LeftMenu.defaultProps = defaultProps;

export default (LeftMenu);
