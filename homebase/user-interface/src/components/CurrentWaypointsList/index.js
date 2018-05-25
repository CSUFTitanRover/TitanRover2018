import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import CircularProgress from '@material-ui/core/CircularProgress';
import InfoIcon from '@material-ui/icons/Info';
import grey from '@material-ui/core/colors/grey';
import { withStyles } from '@material-ui/core/styles';
import { toast } from 'react-toastify';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';
import WaypointList from '../WaypointList/';
import AddWaypointsDialog from '../AddWaypointsDialog/';
import { getClient } from '../../utils/deepstream';

const styles = theme => ({
  container: {
    paddingRight: theme.spacing.unit * 2,
    paddingLeft: theme.spacing.unit * 2,
    background: grey[200],
    height: 'inherit',
    overflow: 'scroll',
  },
  title: {
    marginTop: theme.spacing.unit * 2,
  },
  subheading: {
    display: 'flex',
    marginTop: theme.spacing.unit,
  },
  moreActions: {
    marginTop: theme.spacing.unit,
  },
  deleteAllDialogGridItem: {
    display: 'flex',
    justifyContent: 'center',
  },
  deleteAllDialogGridContainer: {
    marginBottom: theme.spacing.unit * 2,
  },
});

class CurrentWaypointsList extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  state = {
    data: [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]],
    addWaypointsDialogOpen: true,
    deleteAllDialogOpen: false,
    deletingAllWaypoints: false,
  }

  async componentDidMount() {
    this.client = await getClient();
  }

  handleNewPayload = (data) => {
    if (data && data.length > 0) {
      this.setState({ data: data.cp.reverse() });
    }
  }

  openDeleteAllDialog = () => {
    this.setState({ deleteAllDialogOpen: true });
  }

  closeDeleteAllDialog = () => {
    this.setState({ deleteAllDialogOpen: false });
  }

  handleDeleteAll = () => {
    this.setState({ deletingAllWaypoints: true });
    this.client.rpc.make('deleteAllCoordinates', null, (error, result) => {
      this.setState({ deletingAllWaypoints: false });

      if (error) {
        toast.error(error);
      } else {
        this.closeDeleteAllDialog();
        toast.success(result);
      }
    });
  }

  openAddWaypointsDialog = () => {
    this.setState({ addWaypointsDialogOpen: true });
  }

  closeAddWaypointsDialog = () => {
    this.setState({ addWaypointsDialogOpen: false });
  }

  renderWaypointList = (data) => {
    const { classes } = this.props;

    if (data.length === 0) {
      return null;
    }
    return (
      <div className={classes.container}>
        <Typography variant="title" className={classes.title}>Current Waypoints</Typography>
        <Typography variant="subheading" className={classes.subheading}>
          <InfoIcon color="primary" fontSize={12} />
          <span>The first waypoint is the active waypoint</span>
        </Typography>
        <div className={classes.moreActions}>
          <Divider />
          <Button color="primary" onClick={this.openAddWaypointsDialog}>Add Waypoints</Button>
          <Button color="secondary" onClick={this.openDeleteAllDialog}>Delete All</Button>
          <Divider />
        </div>
        <WaypointList data={data} waypointListType="currentPoints" />
      </div>
    );
  }

  renderDeleteAllDialog = () => {
    const { deleteAllDialogOpen, deletingAllWaypoints } = this.state;
    const { classes } = this.props;

    return (
      <Dialog
        open={deleteAllDialogOpen}
        onClose={this.closeDeleteAllDialog}
        aria-labelledby="delete-all-dialog"
      >
        <DialogTitle id="delete-all-dialog">Are you sure you want to delete all waypoints?</DialogTitle>
        <Grid container className={classes.deleteAllDialogGridContainer}>
          <Grid item xs={12} sm={6} className={classes.deleteAllDialogGridItem}>
            <Button
              color="secondary"
              variant="raised"
              onClick={this.closeDeleteAllDialog}
            >
              No
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} className={classes.deleteAllDialogGridItem}>
            <Button color="primary" variant="raised" onClick={this.handleDeleteAll}>
              {deletingAllWaypoints ? <CircularProgress color="default" size={20} /> : 'Yes'}
            </Button>
          </Grid>
        </Grid>
      </Dialog >
    );
  }

  render() {
    const { data, addWaypointsDialogOpen } = this.state;

    return (
      <React.Fragment>
        <DeepstreamRecordProvider
          recordPath="rover/currentPoints"
          onNewPayload={this.handleNewPayload}
        >
          {() => this.renderWaypointList(data)}
        </DeepstreamRecordProvider>
        {this.renderDeleteAllDialog()}
        <AddWaypointsDialog isOpen={addWaypointsDialogOpen} onClose={this.closeAddWaypointsDialog} />
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(CurrentWaypointsList);
