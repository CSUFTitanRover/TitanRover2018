import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

import RoverModel from './RoverModel';
import solve from './solver';

export default class Rover3D extends Component {
  point = null;

  constructor(props, context) {
    super(props, context);

    this.point = null;
    this.syncJoints = true;

    this.state = {
      j1: this.props.j1 * Math.PI / 180,
      j2: this.props.j2 * Math.PI / 180,
      j3: this.props.j3 * Math.PI / 180,
      j4: this.props.j4 * Math.PI / 180,
    };
  }

  handlePickCallback = (point) => {
    this.point = point;
  }

  handleRotation = (change) => {
    this.setState({
      j1: this.state.j1 + change,
    });

    this.syncJoints = false;
  }

  performIK = () => {
    // Solve using IK and desync joints to show fake rover arm
    const newRotations = solve(this.point,
      this.state.j1, this.state.j2, this.state.j3, this.state.j4);

    this.syncJoints = false;
    this.setState({
      j1: newRotations[0],
      j2: newRotations[1],
      j3: newRotations[2],
      j4: newRotations[3],
    });
  }

  sendToRover = () => {
    // TODO: Convert the radians to degrees and send them to the rover or whatever
    // TEST code for this


    // Resync arm with actual arm
    this.syncJoints = true;
    this.componentDidUpdate();
  }

  // Sync the 2 arms together if syncJoints is true
  componentDidUpdate() {
    if (this.state.syncJoints) {
      this.setState({ //eslint-disable-line
        j1: this.props.j1 * Math.PI / 180,
        j2: this.props.j2 * Math.PI / 180,
        j3: this.props.j3 * Math.PI / 180,
        j4: this.props.j4 * Math.PI / 180,
      });
    }
  }

  render() {
    return (
      <Grid container direction={'column'}>
        <Grid item>
          <RoverModel
            handlePickCallback={this.handlePickCallback}
            handleRotation={this.handleRotation}
            j1={this.state.j1}
            j2={this.state.j2}
            j3={this.state.j3}
            j4={this.state.j4}
            realj1={this.props.j1 * Math.PI / 180}
            realj2={this.props.j2 * Math.PI / 180}
            realj3={this.props.j3 * Math.PI / 180}
            realj4={this.props.j4 * Math.PI / 180}
            width={this.props.width}
            height={this.props.height}
          />
        </Grid>

        <Grid item>
          <Grid container style={{ width: this.props.width }} justify={'center'}>
            <Grid item>
              <Button variant={'raised'} color={'primary'} onClick={this.performIK}>Perform IK</Button>
            </Grid>
            <Grid item>
              <span style={{ width: 16, display: 'inline-block' }} />
            </Grid>
            <Grid item>
              <Button variant={'raised'} onClick={this.sendToRover}>Send to Rover</Button>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

Rover3D.propTypes = {
  j1: PropTypes.number.isRequired,
  j2: PropTypes.number.isRequired,
  j3: PropTypes.number.isRequired,
  j4: PropTypes.number.isRequired,
  width: PropTypes.number,
  height: PropTypes.number,
};

Rover3D.defaultProps = {
  width: 400,
  height: 400,
};
