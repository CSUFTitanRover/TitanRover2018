import React, { Component } from 'react';
import PropTypes from 'prop-types';
import has from 'lodash.has';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
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
    data: [],
    addWaypointsDialogOpen: true,
    deleteAllDialogOpen: false,
    deletingAllWaypoints: false,
  }

  async componentDidMount() {
    this.client = await getClient('homebase');
  }

  handleNewPayload = (data) => {
    if (data && has(data, 'cp')) {
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
        <DialogActions>
          <Button onClick={this.closeDeleteAllDialog}>
            Cancel
          </Button>
          <Button color="primary" variant="raised" onClick={this.handleDeleteAll}>
            {deletingAllWaypoints ? <CircularProgress color="default" size={20} /> : 'Yes'}
          </Button>
        </DialogActions>
      </Dialog>
    );
  }

  render() {
    const { addWaypointsDialogOpen, data } = this.state;

    return (
      <React.Fragment>
        <DeepstreamRecordProvider
          recordPath="rover/currentPoints"
          onNewPayload={this.handleNewPayload}
        >
          {() => this.renderWaypointList(data)}
        </DeepstreamRecordProvider>
        {this.renderDeleteAllDialog()}
        <AddWaypointsDialog
          isOpen={addWaypointsDialogOpen}
          onClose={this.closeAddWaypointsDialog}
        />
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(CurrentWaypointsList);
