import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import grey from '@material-ui/core/colors/grey';
import List from '@material-ui/core/List';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';
import { getClient } from '../../utils/deepstream';
import { toast } from 'react-toastify';

const styles = () => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    background: grey[200],
    alignItems: 'center',
  },
});

class CoordinateList extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
    recordPath: PropTypes.string,
  };

  static defaultProps = {
    recordPath: 'rover/currentPoints',
  }

  state = { waypoints: null };

  async componentDidMount() {
    this.client = await getClient();
  }

  handleNewPayload = (data) => {
    console.log(data);
    const { recordPath } = this.props;

    const key = recordPath === 'rover/currentPoints' ? 'cp' : 'pp';

    this.setState({ waypoints: data[key] });
  }

  handleDelete = () => {
    this.client.rpc.make('deleteCoordinate', null, (error, result) => {
      if (error) {
        toast.error(error);
      }

      toast.success(result);
    });
  }


  handleDeleteAll = () => {
    this.client.rpc.make('deleteAllCoordinates', null, (error, result) => {
      if (error) {
        toast.error(error);
      }

      toast.success(result);
    });
  }

  render() {
    const { classes, recordPath } = this.props;
    const { waypoints } = this.state;

    return (
      <div className={classes.container}>
        <DeepstreamRecordProvider recordPath={recordPath} onNewPayload={this.handleNewPayload}>
          {() => (
            <List>
              {waypoints && waypoints.length > 0 && waypoints.map(([lat, lon], key) => (
                <ListItem key={key}>
                  <ListItemText primary={`#${key + 1} - Lat: ${lat}, Lon: ${lon}`} />
                  {key === waypoints.length - 1 && <button onClick={this.handleDelete}>delete</button>}
                </ListItem>
              ))}
            </List>
          )}
        </DeepstreamRecordProvider>

        <button onClick={this.handleDeleteAll}>delete all</button>
      </div >
    );
  }
}

export default withStyles(styles)(CoordinateList);
