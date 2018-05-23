import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Paper from '@material-ui/core/Paper';

const styles = theme => ({
  coordinateInput: {
    padding: theme.spacing.unit * 2,
    marginTop: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit * 2,
  },
});

class CoordinateTypeSelect extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
    handleChange: PropTypes.func.isRequired,
    coordinateType: PropTypes.string.isRequired,
  };

  state = { value: this.props.coordinateType };

  getHelperText = (coordinateType) => {
    switch (coordinateType) {
      case 'decimal-degrees':
        return 'Format: DDD.DDDDD°';
      case 'degrees-minutes-seconds':
        return 'Format: DDD° MM\' SS.S"';
      case 'degrees-decimal-minutes':
        return 'Format: DDD° MM.MMM\'';
      default:
        return 'Format: ';
    }
  }

  handleChange = ({ target }) => {
    this.setState({ value: target.value });
    this.props.handleChange(target.value);
  }

  render() {
    const { value } = this.state;
    const { classes } = this.props;

    return (
      <Paper square={false} className={classes.coordinateInput}>
        <FormControl>
          <InputLabel htmlFor="coordinate-type">Coordinate Type</InputLabel>
          <Select
            value={value}
            onChange={this.handleChange}
            inputProps={{
              name: 'coordinate-type',
              id: 'coordinate-type',
            }}
          >
            <MenuItem value="decimal-degrees">Decimal Degrees</MenuItem>
            <MenuItem value="degrees-minutes-seconds">Degrees, Minutes and Seconds</MenuItem>
            <MenuItem value="degrees-decimal-minutes">Degrees and Decimal Minutes</MenuItem>
          </Select>
          <FormHelperText>{this.getHelperText(value)}</FormHelperText>
        </FormControl>
      </Paper>
    );
  }
}

export default withStyles(styles)(CoordinateTypeSelect);
