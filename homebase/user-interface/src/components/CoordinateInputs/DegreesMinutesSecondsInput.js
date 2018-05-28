import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';
import Paper from '@material-ui/core/Paper';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import { convertDMSToDD } from '../../utils/coordinates';

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
});

class DegreesMinutesSecondsInput extends Component {
  static propTypes = {
    handleChange: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  };

  state = {
    latitude: {
      degrees: '',
      minutes: '',
      seconds: '',
      direction: 'north',
    },
    longitude: {
      degrees: '',
      minutes: '',
      seconds: '',
      direction: 'west',
    },
  }

  isEmpty = obj => (
    obj.degrees.length === 0 ||
    obj.minutes.length === 0 ||
    obj.seconds.length === 0 ||
    obj.seconds.direction === 0
  )

  handleLatitudeChange = ({ target }) => {
    const { latitude } = this.state;
    latitude[target.name] = target.value;
    this.setState({ latitude });

    // if the coordinate is not empty
    // then compute the final decimal-degree value
    if (!this.isEmpty(latitude)) {
      const computedLatitude = convertDMSToDD(latitude);

      this.props.handleChange({ finalLatitude: computedLatitude });
    }
  }

  handleLongitudeChange = ({ target }) => {
    const { longitude } = this.state;
    longitude[target.name] = target.value;
    this.setState({ longitude });

    // if the coordinate is not empty
    // then compute the final decimal-degree value
    if (!this.isEmpty(longitude)) {
      const computedLongitude = convertDMSToDD(longitude);

      this.props.handleChange({ finalLongitude: computedLongitude });
    }
  }

  render() {
    const labels = ['degrees', 'minutes', 'seconds'];
    const placeholders = ['DDD°', 'MM\'', 'SS.S"'];
    const { classes } = this.props;

    return (
      <React.Fragment>
        <Paper square className={classes.coordinateInput}>
          <Typography variant="title">Latitude</Typography>
          <Typography variant="caption">(only the numerical values are required)</Typography>
          {labels.map((label, i) => (
            <FormControl className={classes.input}>
              <TextField
                key={`latitude-${label}`}
                type="number"
                step="any"
                id={`latitude-${label}`}
                label={label}
                placeholder={placeholders[i]}
                name={`${label}`}
                onChange={this.handleLatitudeChange}
                value={this.state.latitude[label]}
                margin="normal"
              />
            </FormControl>
          ))}
          <FormControl className={classes.input}>
            <InputLabel htmlFor="latitude-direction">Direction</InputLabel>
            <Select
              value={this.state.latitude.direction}
              onChange={this.handleLatitudeChange}
              inputProps={{
                name: 'direction',
                id: 'latitude-direction',
              }}
            >
              <MenuItem value="north">North</MenuItem>
              <MenuItem value="east">East</MenuItem>
              <MenuItem value="south">South</MenuItem>
              <MenuItem value="west">West</MenuItem>
            </Select>
          </FormControl>
        </Paper>

        <Paper square className={classes.coordinateInput}>
          <Typography variant="title">Longitude</Typography>
          <Typography variant="caption">(only the numerical values are required)</Typography>
          {labels.map((label, i) => (
            <FormControl className={classes.input}>
              <TextField
                key={`longitude-${label}`}
                type="number"
                step="any"
                id={`longitude-${label}`}
                label={label}
                placeholder={placeholders[i]}
                name={`${label}`}
                onChange={this.handleLongitudeChange}
                value={this.state.longitude[label]}
                margin="normal"
              />
            </FormControl>
          ))}
          <FormControl className={classes.input}>
            <InputLabel htmlFor="longitude-direction">Direction</InputLabel>
            <Select
              value={this.state.longitude.direction}
              onChange={this.handleLongitudeChange}
              inputProps={{
                name: 'direction',
                id: 'longitude-direction',
              }}
            >
              <MenuItem value="north">North</MenuItem>
              <MenuItem value="east">East</MenuItem>
              <MenuItem value="south">South</MenuItem>
              <MenuItem value="west">West</MenuItem>
            </Select>
          </FormControl>
        </Paper>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(DegreesMinutesSecondsInput);
