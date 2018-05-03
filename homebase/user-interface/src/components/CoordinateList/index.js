import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import PropTypes from 'prop-types';
import grey from 'material-ui/colors/grey';
import List, {
  ListItem,
  ListItemAvatar,
  ListItemIcon,
  ListItemSecondaryAction,
  ListItemText,
} from 'material-ui/List';
import DeepstreamRecordProvider from '../../utils/DeepstreamRecordProvider/';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    background: grey[200],
    alignItems: 'center'
  },
});

class CoordinateList extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  state = { waypoints: null };

  handleNewPayload = (data) => {
    this.setState({ waypoints: data })
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
    )
  }
}

export default withStyles(styles)(CoordinateList);