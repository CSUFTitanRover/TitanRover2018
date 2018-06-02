import React, { Component } from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import convert from 'convert-units';
import TextField from '@material-ui/core/TextField';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import { getClient, getRecordSnapshot } from '../../utils/deepstream';

const toRadians = value => value * (Math.PI / 180);
const toDegrees = value => value * (180 / Math.PI);

const styles = theme => ({
  coordinateInput: {
    padding: theme.spacing.unit * 2,
    marginTop: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit * 2,
  },
  input: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
  },
  distanceInput: {
    display: 'flex',
    flexFlow: 'column',
  },
  result: {
    marginTop: theme.spacing.unit,
  },
});

class HeadingLocationOffsetHeadingInput extends Component {
  static propTypes = {
    handleChange: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  };

  state = {
    offsetHeading: undefined,
    distance: undefined,
    distanceType: 'ft',
  }

  async componentDidMount() {
    this.client = await getClient('homebase');
  }

  handleBaseChange = () => {
    const { convertedDistance, offsetHeading } = this.state;
    if (convertedDistance && offsetHeading) {
      const calculatedHeading = this.calculateHeading(offsetHeading);
      const { latitude, longitude } = this.calculateLocation(calculatedHeading, convertedDistance);
      this.props.handleChange({ finalLatitude: latitude, finalLongitude: longitude });
    }
  }

  calculateHeading = (offsetHeading) => {
    // const { heading } = getRecordSnapshot(this.client, 'rover/imu');
    const heading = 70;

    return (heading + offsetHeading) % 360;
  }

  calculateLocation = (heading, distance) => {
    // const currentLocation = getRecordSnapshot(this.client, 'rover/gnss');
    const currentLocation = { latitude: -33.2658745, longitude: 127.0641258 };
    const headingRadians = toRadians(heading);
    const radius = 6371;
    const computedDistance = distance / 100000.0;
    const currentLatitude = toRadians(currentLocation.latitude);
    const currentLongitude = toRadians(currentLocation.longitude);

    let calculatedLatitude = Math.asin(
      Math.sin(currentLatitude) * Math.cos(computedDistance / radius) +
      Math.cos(currentLatitude) * Math.sin(computedDistance / radius) * Math.cos(headingRadians),
    );

    let calculatedLongitude = currentLongitude + Math.atan2(
      Math.sin(headingRadians) * Math.sin(computedDistance / radius) * Math.cos(currentLatitude),
      Math.cos(computedDistance / radius) - Math.sin(currentLatitude) * Math.sin(calculatedLatitude),
    );

    calculatedLatitude = toDegrees(calculatedLatitude);
    calculatedLongitude = toDegrees(calculatedLongitude);

    return { latitude: calculatedLatitude, longitude: calculatedLongitude };
  }

  handleDistanceChange = ({ target }) => {
    const { distanceType } = this.state;
    const distance = target.value;
    const convertedDistance = convert(distance).from(distanceType).to('cm');

    this.setState({ distance, convertedDistance },
      () => {
        this.handleBaseChange();
      });
  }

  handleDistanceTypeChange = ({ target }) => {
    const { distance } = this.state;
    const distanceType = target.value;
    const convertedDistance = convert(distance).from(distanceType).to('cm');

    this.setState({ distanceType, convertedDistance },
      () => {
        this.handleBaseChange();
      });
  }

  handleOffsetHeadingChange = ({ target }) => {
    this.setState({ offsetHeading: target.value },
      () => {
        this.handleBaseChange();
      });
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Paper square className={classes.coordinateInput}>
          <Typography variant="title">Offset Heading</Typography>
          <FormControl>
            <TextField
              type="number"
              step="any"
              id="offsetHeading"
              label="offset heading"
              name="offsetHeading"
              onChange={this.handleOffsetHeadingChange}
              value={this.state.offsetHeading}
              margin="normal"
              placeholder="DDD°"
            />
          </FormControl>
        </Paper>

        <Paper square className={cn(classes.coordinateInput, classes.distanceInput)}>
          <Typography variant="title">Distance</Typography>
          <FormControl>
            <TextField
              type="number"
              step="any"
              id="distance"
              label="distance"
              name="distance"
              onChange={this.handleDistanceChange}
              value={this.state.distance}
              margin="normal"
              placeholder="DDD.DD"
            />
          </FormControl>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="distanceType">Distance Type</InputLabel>
            <Select
              value={this.state.distanceType}
              onChange={this.handleDistanceTypeChange}
              inputProps={{
                name: 'distanceType',
                id: 'distanceType',
              }}
            >
              <MenuItem value="ft">feet</MenuItem>
              <MenuItem value="yd">yard</MenuItem>
              <MenuItem value="mi">miles</MenuItem>
              <MenuItem value="m">meters</MenuItem>
              <MenuItem value="km">kilometers</MenuItem>
            </Select>
          </FormControl>
          {this.state.distance && this.state.distanceType && (
            <Typography className={classes.result} variant="caption">Result: {this.state.convertedDistance} cm</Typography>
          )}
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(HeadingLocationOffsetHeadingInput);
