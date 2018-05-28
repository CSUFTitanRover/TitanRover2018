import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Switch from '@material-ui/core/Switch';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import grey from '@material-ui/core/colors/grey';
import { withStyles } from '@material-ui/core/styles';
import { toast } from 'react-toastify';
import { getClient } from '../../utils/deepstream';
import {
  HIGH_SPEED,
  LOW_SPEED,
} from '../../utils/motor_constants';

const styles = theme => ({
  verticalDivider: {
    marginRight: theme.spacing.unit,
    marginLeft: theme.spacing.unit,
    width: 2,
    height: '100%',
    border: '1px solid',
    borderColor: grey[500],
  },
});

class MotorSpeedSwitch extends Component {
  static propTypes = {
    address: PropTypes.string.isRequired,
    jointName: PropTypes.string,
    classes: PropTypes.object.isRequired,
  }

  state = { highSpeed: true }

  async componentDidMount() {
    this.client = await getClient();
  }

  handleChange = () => {
    const { highSpeed } = this.state;
    const { address } = this.props;

    const newSpeed = !highSpeed;
    const data = {
      address,
      value: newSpeed ? HIGH_SPEED : LOW_SPEED,
    };

    this.client.rpc.make('changeMotorSpeed', data, (error, result) => {
      if (error) {
        toast.error(error);
      } else {
        // this would be done by the tcp server!
        this.setState({ highSpeed: newSpeed });
        toast.success(result);
      }
    });

    // this.setState(prevState => ({
    //   highSpeed: !prevState.highSpeed,
    // }));
  }

  render() {
    const { classes, jointName } = this.props;
    const { highSpeed } = this.state;
    return (
      <React.Fragment>
        <ListItemText
          primary={`${jointName}: ${highSpeed ? 'High' : 'Low'} Speed`}
        />
        <ListItemSecondaryAction>
          <Switch
            checked={highSpeed}
            onChange={this.handleChange}
            color="primary"
          />
        </ListItemSecondaryAction>
      </React.Fragment>

    );
  }
}

export default withStyles(styles)(MotorSpeedSwitch);
