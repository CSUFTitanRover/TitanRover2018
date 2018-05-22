import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Stepper from '@material-ui/core/Stepper';
import StepLabel from '@material-ui/core/StepLabel';
import Step from '@material-ui/core/Step';
import grey from '@material-ui/core/colors/grey';
import { toast } from 'react-toastify';
import { getClient, getRecord, syncInitialRecordState } from '../../utils/deepstream';
import CoordinateTypeSelect from '../CoordinateTypeSelect/';

const styles = theme => ({
  form: {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    padding: theme.spacing.unit * 2,
  },
  stepper: {
    background: grey[50],
  },
  contentWrapper: {
    background: grey[200],
  },
  buttons: {
    padding: theme.spacing.unit * 2,
    display: 'flex',
    justifyContent: 'space-between',
  },
  actionButton: {
    justifySelf: 'flex-end',
  },
});

class GpsCoordinator extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  state = {
    activeStep: 0,
    coordinateType: 'decimal-degrees',
  };

  steps = [
    'Select Type',
    'Waypoint Input',
    'Confirm',
  ];

  handleCoordinateTypeChange = (value) => {
    this.setState({ coordinateType: value });
  }

  getStepContent = (stepIndex) => {
    const { coordinateType } = this.state;

    switch (stepIndex) {
      case 0:
        return (
          <CoordinateTypeSelect
            coordinateType={coordinateType}
            handleChange={this.handleCoordinateTypeChange}
          />
        );
      case 1:
        return '<Input />';
      case 2:
        return '<Confirm />';
      default:
        return 'Error: Unknown step.';
    }
  }

  handleNext = () => {
    this.setState(prevState => ({
      activeStep: prevState.activeStep + 1,
    }));
  };

  handleBack = () => {
    this.setState(prevState => ({
      activeStep: prevState.activeStep - 1,
    }));
  };

  handleReset = () => {
    this.setState({
      activeStep: 0,
    });
  };


  async componentDidMount() {
    this.client = await getClient('rover');
    this.waypointsRecord = await getRecord(this.client, 'rover/waypoints');
    const initialState = [];
    await syncInitialRecordState.call(this, this.client, 'rover/waypoints', initialState);
  }

  renderContent = ({ activeStep, classes }) => (
    <div className={classes.contentWrapper}>
      <form className={classes.form} noValidate autoComplete="off" >
        {this.getStepContent(activeStep)}
      </form>
      <div className={classes.buttons}>
        <Button
          variant="raised"
          color="default"
          disabled={activeStep === 0}
          onClick={this.handleBack}
        >
          Back
        </Button>
        {activeStep === this.steps.length - 1 ? (
          <Button
            variant="raised"
            color="primary"
            className={classes.actionButton}
            onClick={this.handleNext}
          >
            Finish
          </Button>
        ) : (
          <Button
            variant="raised"
            color="primary"
            className={classes.actionButton}
            onClick={this.handleNext}
          >
              Next
          </Button>
        )}
      </div>
    </div>
  )


  render() {
    const { activeStep } = this.state;
    const { classes } = this.props;

    return (
      <React.Fragment>
        <Stepper activeStep={activeStep} alternativeLabel className={classes.stepper}>
          {this.steps.map(label => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <div>
          {this.renderContent({ activeStep, classes })}
        </div>
      </React.Fragment >
    );
  }
}

export default withStyles(styles)(GpsCoordinator);
