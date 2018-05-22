import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import grey from '@material-ui/core/colors/grey';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    background: grey[200],
    alignItems: 'center',
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
    maxHeight: 20,
  },
});

class CoordinateTypeSelect extends PureComponent {
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
      <FormControl className={classes.formControl}>
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
    );
  }
}

export default withStyles(styles)(CoordinateTypeSelect);
