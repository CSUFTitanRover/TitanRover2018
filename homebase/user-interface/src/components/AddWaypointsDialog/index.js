import React, { Component } from 'react';
import PropTypes from 'prop-types';
import isEmpty from 'lodash.isempty';
import { toast } from 'react-toastify';
import Dialog from '@material-ui/core/Dialog';
import Paper from '@material-ui/core/Paper';
import Slide from '@material-ui/core/Slide';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import SvgIcon from '@material-ui/core/SvgIcon';
import CloseIcon from '@material-ui/icons/Close';
import CircularProgress from '@material-ui/core/CircularProgress';
import grey from '@material-ui/core/colors/grey';
import { withStyles } from '@material-ui/core/styles';
import Coordinator from '../Coordinator/';
import TemporaryWaypointsList from '../TemporaryWaypointsList/';
import { getClient } from '../../utils/deepstream';

const RightArrowIcon = props => (
  <SvgIcon {...props}>
    <path d="M16.01 11H4v2h12.01v3L20 12l-3.99-4z" />
  </SvgIcon>
);

const styles = theme => ({
  column: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    // height: '100vh',
  },
  gridContainer: {
    background: grey[200],
    padding: theme.spacing.unit * 2,
    height: '100vh',
  },
  gridItemClose: {
    display: 'flex',
    justifyContent: 'flex-end',
    width: '100%',
    marginBottom: theme.spacing.unit * 2,
  },
  arrowForwardIcon: {
    width: 80,
    height: 80,
    color: grey[500],
  },
  coordinatorContainer: {
    width: '100%',
    height: '100%',
    display: 'flex',
    alignSelf: 'flex-start',
  },
  paperItem: {
    height: '100%',
  },
  commitContainer: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  commitButton: {
    margin: theme.spacing.unit * 2,
    transition: theme.transitions.create(['height', 'width'], {
      easing: theme.transitions.easing.easeInOut,
      duration: theme.transitions.duration.standard,
    }),
  },
});

class AddWaypointsDialog extends Component {
  static propTypes = {
    isOpen: PropTypes.bool,
    onClose: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  }

  static defaultProps = {
    isOpen: false,
  }

  state = { isCommiting: false }

  async componentDidMount() {
    this.client = await getClient();
  }

  handleCommitClick = () => {
    this.client.record.snapshot('temp/waypoints', (error, data) => {
      if (error) {
        toast.error('There was an issue grabbing the temporary waypoints data from deepstream.');
      } else {
        if (isEmpty(data)) {
          toast.error('Error: No waypoints to commit!');
          return;
        }

        const transformedData = data.map(item => item.content);
        const computedDataString = transformedData.reduce((acc, curr) => (
          `${curr[0]},${curr[1]},${acc}`),
        );

        console.info('computedDataString for temp waypoints:');
        console.info(computedDataString);

        this.setState({ isCommiting: true });
        this.client.rpc.make('addCoordinate', computedDataString, (rpcError, result) => {
          if (rpcError) {
            toast.error(rpcError);
          }

          // clear the temp waypoints record
          this.client.record.setData('temp/waypoints', []);
          this.setState({ isCommiting: false });
          toast.success(result);
          this.handleClose();
        });
      }
    });
  }

  handleClose = () => {
    const { onClose } = this.props;
    onClose();
  }

  transition = props => <Slide direction="up" {...props} />

  render() {
    const { isCommiting } = this.state;
    const { isOpen, classes } = this.props;

    return (
      <Dialog
        fullScreen
        open={isOpen}
        onClose={this.handleClose}
        TransitionComponent={this.transition}
      >
        <div className={classes.gridContainer}>
          <Grid container>
            <Grid item className={classes.gridItemClose} >
              <Tooltip title="Exit" placement="left">
                <IconButton aria-label="Exit" onClick={this.handleClose}>
                  <CloseIcon />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>

          <Grid container>
            <Grid item xs={5}>
              <Paper className={classes.paperItem} elevation={8} square={false}>
                <Coordinator />
              </Paper>
            </Grid>

            <Grid item xs={2} className={classes.column}>
              <div>
                <RightArrowIcon className={classes.arrowForwardIcon} />
              </div>
            </Grid>

            <Grid item xs={5}>
              <Paper className={classes.paperItem} elevation={8} square={false}>
                <TemporaryWaypointsList />
                <Divider />
                <div className={classes.commitContainer}>
                  <Button
                    color="primary"
                    variant="raised"
                    className={classes.commitButton}
                    onClick={this.handleCommitClick}
                  >
                    {isCommiting ? <CircularProgress size={20} color="default" /> : 'Commit Staged Waypoints'}
                  </Button>
                </div>
              </Paper>
            </Grid>
          </Grid>
        </div>
      </Dialog >
    );
  }
}

export default withStyles(styles)(AddWaypointsDialog);
