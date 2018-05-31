import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Stepper from '@material-ui/core/Stepper';
import StepLabel from '@material-ui/core/StepLabel';
import Step from '@material-ui/core/Step';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import grey from '@material-ui/core/colors/grey';
import green from '@material-ui/core/colors/green';
import InfoIcon from '@material-ui/icons/Info';
import cn from 'classnames';
import { toast } from 'react-toastify';
import { getClient } from '../../utils/deepstream';
import CoordinateTypeSelect from '../CoordinateTypeSelect/';
import { DecimalDegreeInput, DegreesMinutesSecondsInput, DegreesDecimalMinutesInput } from '../CoordinateInputs/';

const styles = theme => ({
  form: {
    display: 'flex',
    flexWrap: 'wrap',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: theme.spacing.unit * 2,
  },
  stepper: {
    background: grey[100],
  },
  title: {
    padding: theme.spacing.unit * 2,
    background: theme.palette.primary.main,
    color: grey[50],
  },
  buttons: {
    padding: theme.spacing.unit * 2,
    display: 'flex',
    justifyContent: 'space-between',
  },
  actionButton: {
    justifySelf: 'flex-end',
  },
  finalCoordinatePaper: {
    padding: theme.spacing.unit * 2,
    marginTop: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit * 2,
  },
  finalCoordinate: {
    padding: theme.spacing.unit * 2,
  },
  finishButton: {
    background: green[500],
    '&:hover': {
      background: green[700],
    },
  },
  finalInfo: {
    display: 'flex',
    alignItems: 'center',
  },
  infoIcon: {
    color: grey[500],
  },
  infoText: {
    alignSelf: 'flex-start',
    marginLeft: theme.spacing.unit,
  },
});

class Coordinator extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  state = {
    activeStep: 0,
    coordinateType: 'decimal-degrees',
    finalLatitude: null,
    finalLongitude: null,
  };

  steps = [
    'Select Type',
    'Coordinate Input',
    'Confirm',
  ];

  handleCoordinateTypeChange = (value) => {
    this.setState({ coordinateType: value });
  }

  handleFinalCoordinateChange = (data) => {
    this.setState({ ...data });
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
      coordinateType: 'decimal-degrees',
      finalLatitude: null,
      finalLongitude: null,
    });
  };

  handleFinish = () => {
    const { finalLatitude, finalLongitude } = this.state;

    if (!finalLatitude || !finalLongitude) {
      toast.error('Error: Cannot add an empty coordinate!');
    } else {
      const data = [finalLatitude, finalLongitude];

      this.client.event.emit('temp/waypoints:add', data);
      this.handleReset();

      // use this in the commit button on the dialog
      // const data = `${finalLatitude},${finalLongitude}`;
      // this.client.rpc.make('addCoordinate', data, (error, result) => {
      //   if (error) {
      //     toast.error(error);
      //   }

      //   toast.success(result);
      //   this.handleReset();
      // });
    }
  }

  getStepContent = (stepIndex, classes) => {
    const { coordinateType, finalLatitude, finalLongitude } = this.state;

    switch (stepIndex) {
      case 0:
        return (
          <CoordinateTypeSelect
            coordinateType={coordinateType}
            handleChange={this.handleCoordinateTypeChange}
          />
        );
      case 1:
        if (coordinateType === 'decimal-degrees') {
          return (
            <DecimalDegreeInput
              handleChange={this.handleFinalCoordinateChange}
            />
          );
        } else if (coordinateType === 'degrees-minutes-seconds') {
          return (
            <DegreesMinutesSecondsInput
              handleChange={this.handleFinalCoordinateChange}
            />
          );
        } else if (coordinateType === 'degrees-decimal-minutes') {
          return (
            <DegreesDecimalMinutesInput
              handleChange={this.handleFinalCoordinateChange}
            />
          );
        }
        throw Error('The coordinate type must be selected in order to show the coordinate input');

      case 2:
        return (
          <React.Fragment>
            <Typography variant="title">Awesome, does this look correct?</Typography>

            <Paper square={false} className={classes.finalCoordinatePaper}>
              <Typography variant="subheading" className={classes.finalInfo}>
                <InfoIcon className={classes.infoIcon} />
                <span className={classes.infoText}>
                  Coordinates are formatted in decimal-degrees
                </span>
              </Typography>
              <Typography variant="headline" className={classes.finalCoordinate}>
                Latitude: <strong>{finalLatitude}</strong>
              </Typography>
              <Typography variant="headline" className={classes.finalCoordinate}>
                Longitude: <strong>{finalLongitude}</strong>
              </Typography>
            </Paper>
          </React.Fragment>
        );
      default:
        return 'Error: Unknown step.';
    }
  }

  renderContent = ({ activeStep, classes }) => (
    <div className={classes.contentWrapper}>
      <form className={classes.form} noValidate autoComplete="off" >
        {this.getStepContent(activeStep, classes)}
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
            className={cn(classes.actionButton, classes.finishButton)}
            onClick={this.handleFinish}
          >
            Add Coordinate
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

  async componentDidMount() {
    this.client = await getClient('homebase');
  }

  render() {
    const { activeStep } = this.state;
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <Typography variant="title" className={classes.title}>Add a Waypoint</Typography>
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
      </div >
    );
  }
}

export default withStyles(styles)(Coordinator);
