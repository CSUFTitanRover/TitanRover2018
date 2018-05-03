import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import PropTypes from 'prop-types';
import grey from 'material-ui/colors/grey';
import { getClient, getRecord, syncInitialRecordState } from '../../utils/deepstream';
import { toast } from 'react-toastify';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    background: grey[200],
    alignItems: 'center'
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  menu: {
    width: 200,
  },
  button: {
    margin: theme.spacing.unit,
    maxHeight: 20
  }
});

class GpsCoordinator extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  async componentDidMount() {
    this.client = await getClient('rover');
    this.waypointsRecord = await getRecord(this.client, 'rover/waypoints');
    const initialState = [];
    await syncInitialRecordState.call(this, this.client, 'rover/waypoints', initialState);
  }

  handleSubmit = (event) => {
    event.preventDefault();
    const lat = this.latitudeRef.value;
    const lon = this.longitudeRef.value;

    if (!lat || !lon) {
      toast.error('Latitude or Longitude cannot be empty!')
      return;
    }

    const waypoints = this.waypointsRecord.get();
    waypoints.push({ lat, lon });
    console.log(waypoints, typeof waypoints)
    this.waypointsRecord.set(waypoints);

    console.log(`Added the following to deepstream... Lat: ${lat}, Lon:${lon}`);

    this.latitudeRef.value = null;
    this.longitudeRef.value = null;
  }

  render() {
    const { classes } = this.props;

    return (
      <form className={classes.container} noValidate autoComplete="off" onSubmit={this.handleSubmit}>
        <TextField
          inputRef={(ref) => { this.latitudeRef = ref }}
          id="latitude"
          label="Latitude"
          className={classes.textField}
          margin="normal"
          type="number"
          step="any"
          required
        />
        <TextField
          inputRef={(ref) => { this.longitudeRef = ref }}
          id="longitude"
          label="Longitude"
          className={classes.textField}
          margin="normal"
          type="number"
          step="any"
          required
        />
        <Button
          type="submit"
          variant="raised"
          color="primary"
          size="small"
          className={classes.button}>
          Add Coordinate
        </Button>
      </form>
    )
  }
}

export default withStyles(styles)(GpsCoordinator);