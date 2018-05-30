import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { toast } from 'react-toastify';
import { getClient } from '../../utils/deepstream';

class JointRotationInput extends Component {
  static propTypes = {
    address: PropTypes.string.isRequired,
    jointName: PropTypes.string,
  }

  state = { rotation: 0 }

  async componentDidMount() {
    this.client = await getClient();
  }

  handleChange = ({ target }) => {
    this.setState({ rotation: target.value });
  }

  handleApply = () => {
    const { rotation } = this.state;
    const { address } = this.props;

    const data = {
      address,
      direction: rotation < 0 ? 2 : 1,
      value: rotation,
    };

    this.client.rpc.make('rotateMotor', data, (error, result) => {
      if (error) {
        toast.error(error);
      } else {
        toast.success(result);
      }
    });
  }

  render() {
    const { jointName } = this.props;
    const { rotation } = this.state;
    return (
      <React.Fragment>
        <TextField
          id="rotation"
          label={`${jointName} Rotation`}
          value={rotation}
          onChange={this.handleChange}
          type="number"
          margin="dense"
        />
        <Button
          color="primary"
          variant="raised"
          size="small"
          style={{ margin: '10px 0 0 5px' }}
          onClick={this.handleApply}
        >
          Apply
        </Button>
      </React.Fragment>
    );
  }
}

export default JointRotationInput;
