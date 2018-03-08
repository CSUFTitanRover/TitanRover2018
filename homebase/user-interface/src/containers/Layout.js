import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Grid from 'material-ui/Grid';
import { ToastContainer, toast } from 'react-toastify';
import TopBar from './TopBar/';
import LeftMenu from './LeftMenu/';

const propTypes = {
  /** Any child element that is renderable e.g. Text, HTML, etc. */
  children: PropTypes.node.isRequired,
  /** current active state of left menu */
  leftMenuActive: PropTypes.bool.isRequired,
  /** this prop is supplied via withStyles() */
  classes: PropTypes.object.isRequired,
};

const defaultProps = {
  children: null,
  leftMenuActive: false,
  classes: {},
};

const mapStateToProps = state => ({ leftMenuActive: state.leftMenuActive });

const drawerWidth = 250;

const styles = theme => ({
  topBar: {
    width: '100vw',
    height: 65,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  topBarShift: {
    width: `calc(100vw - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaper: {
    width: drawerWidth,
  },
  content: {
    marginLeft: 0,
    width: '100%',
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  contentShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
});

/** The Layout wraps any child components passed to it with
 * the TopBar and LeftMenu.
 */
class Layout extends Component {
  render() {
    const { leftMenuActive, classes } = this.props;

    return (
      <Grid container spacing={0}>
        <ToastContainer position={toast.POSITION.TOP_CENTER} />

        <Grid item xs={12}>
          <TopBar classNames={classNames(classes.topBar, leftMenuActive && classes.topBarShift)} />
          <LeftMenu drawerPaperClassNames={classNames(classes.drawerPaper)} />
        </Grid>

        <Grid item xs={12}>
          <main className={classNames(classes.content, leftMenuActive && classes.contentShift)}>
            {this.props.children}
          </main>
        </Grid>
      </Grid>
    );
  }
}

Layout.propTypes = propTypes;
Layout.defaultProps = defaultProps;

const LayoutWithStyles = withStyles(styles)(Layout);

export default connect(mapStateToProps)(LayoutWithStyles);
