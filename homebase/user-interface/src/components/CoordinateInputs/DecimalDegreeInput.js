import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

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

class DecimalDegreeInput extends Component {
  static propTypes = {
    handleChange: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  };

  state = {
    latitude: '',
    longitude: '',
  }

  handleLatitudeChange = ({ target }) => {
    const latitude = target.value;
    this.setState({ latitude });

    const finalLatitude = parseFloat(latitude);

    this.props.handleChange({ finalLatitude });
  }

  handleLongitudeChange = ({ target }) => {
    const longitude = target.value;
    this.setState({ longitude });

    const finalLongitude = parseFloat(longitude);

    this.props.handleChange({ finalLongitude });
  }

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
        <Paper square className={classes.coordinateInput}>
          <Typography variant="title">Latitude</Typography>
          <Typography variant="caption">(only the numerical values are required)</Typography>
          <FormControl>
            <TextField
              type="number"
              step="any"
              id="latitude"
              label="decimal-degrees"
              onChange={this.handleLatitudeChange}
              value={this.state.latitude}
              margin="normal"
              placeholder="±DDD.DDDDD°"
            />
          </FormControl>
        </Paper>

        <Paper square className={classes.coordinateInput}>
          <Typography variant="title">Longitude</Typography>
          <Typography variant="caption">(only the numerical values are required)</Typography>
          <FormControl>
            <TextField
              type="number"
              step="any"
              id="longitude"
              label="decimal-degrees"
              name="longitude"
              onChange={this.handleLongitudeChange}
              value={this.state.longitude}
              margin="normal"
              placeholder="±DDD.DDDDD°"
            />
          </FormControl>
        </Paper>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(DecimalDegreeInput);
