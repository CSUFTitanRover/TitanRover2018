import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import grey from '@material-ui/core/colors/grey';
import List from '@material-ui/core/List';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';

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
  };

  state = { waypoints: null };

  handleNewPayload = (data) => {
    this.setState({ waypoints: data });
  }

  render() {
    const { classes } = this.props;
    const { waypoints } = this.state;

    return (
      <div className={classes.container}>
        <DeepstreamRecordProvider client="rover" recordPath="rover/waypoints" onNewPayload={this.handleNewPayload}>
          {() => (
            <List>
              {waypoints && waypoints.length > 0 && waypoints.map(({ lat, lon }, key) => (
                <ListItem key={key}>
                  <ListItemText primary={`#${key + 1} - Lat: ${lat}, Lon: ${lon}`} />
                </ListItem>
              ))}
            </List>
          )}
        </DeepstreamRecordProvider>
      </div>
    );
  }
}

export default withStyles(styles)(CoordinateList);
