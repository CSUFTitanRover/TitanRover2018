import React, { Component } from 'react';
import PropTypes from 'prop-types';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';
import CircularProgress from '@material-ui/core/CircularProgress';
import grey from '@material-ui/core/colors/grey';
import { toast } from 'react-toastify';
import { withStyles } from '@material-ui/core/styles';
import { getClient } from '../../utils/deepstream';

const styles = theme => ({
  container: {
    paddingRight: theme.spacing.unit * 2,
    paddingLeft: theme.spacing.unit * 2,
    background: grey[200],
    height: 'inherit',
    overflow: 'scroll',
  },
  listItem: {
    marginTop: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit * 2,
    background: theme.palette.background.paper,
    boxShadow: theme.shadows[2],
  },
  deleteIcon: {
    marginLeft: theme.spacing.unit,
  },
});

class WaypointList extends Component {
  static propTypes = {
    data: PropTypes.arrayOf(PropTypes.array),
    classes: PropTypes.object.isRequired,
    waypointListType: PropTypes.oneOf(['currentPoints', 'previousPoints']),
  };

  static defaultProps = {
    data: [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]],
    waypointListType: 'currentPoints',
  }

  client = null;

  state = { isDeletingWaypoint: false };

  async componentDidMount() {
    const { waypointListType } = this.props;

    if (waypointListType === 'currentPoints') {
      this.client = await getClient();
    }
  }

  handleWaypointDelete = (latitude, longitude) => () => {
    if (this.client) {
      this.setState({ isDeletingWaypoint: true });
      const computedData = `${latitude},${longitude}`;

      this.client.rpc.make('deleteCoordinate', computedData, (error, result) => {
        if (error) {
          toast.error(error);
        }

        toast.success(result);
        this.setState({ isDeletingWaypoint: false });
      });
    } else {
      toast.error('There was an issue connecting to Deepstream to send the rpc request.');
    }
  }

  renderAdditionalContent = (latitude, longitude) => {
    const { classes } = this.props;
    const { isDeletingWaypoint } = this.state;

    if (isDeletingWaypoint) {
      return <CircularProgress className={classes.progress} />;
    }

    return (
      <Button
        className={classes.button}
        variant="raised"
        color="secondary"
        onClick={this.handleWaypointDelete(latitude, longitude)}
      >
        Delete
        <DeleteIcon className={classes.deleteIcon} />
      </Button>
    );
  }

  renderListItem = (latitude, longitude, index) => {
    const { waypointListType, classes } = this.props;

    const shouldShowDeleteButton = waypointListType === 'currentPoints';

    return (
      <ListItem key={`${latitude}-${longitude}`} className={classes.listItem}>
        <ListItemText>{`${index + 1}. `}<strong>Latitude: </strong>{`${latitude}, `}<strong>Longitude: </strong>{longitude}</ListItemText>
        {shouldShowDeleteButton && this.renderAdditionalContent(latitude, longitude)}
      </ListItem>
    );
  }

  render() {
    const { data, classes } = this.props;
    const totalLength = data.length;

    return (
      <div className={classes.container}>
        <List>
          {data.map(([latitude, longitude], index) => (
            this.renderListItem(latitude, longitude, index, totalLength)
          ))}
        </List>
      </div>
    );
  }
}

export default withStyles(styles)(WaypointList);
