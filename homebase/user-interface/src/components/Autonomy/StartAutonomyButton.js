import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import Modal from '@material-ui/core/Modal';
import { withStyles } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import PropTypes from 'prop-types';

const styles = theme => ({
  paper: {
    backgroundColor: theme.palette.background.paper,
    boxShadow: theme.shadows[5],
    padding: theme.spacing.unit * 4,
  },
  checkCircle: {
    width: 48,
    height: 48,
    color: green[500],
  },
});

class StartAutonomyButton extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  state = { open: false }

  handleModalOpen = () => {
    this.setState({ open: true });
  };

  handleModalClose = () => {
    this.setState({ open: false });
  };

  startAutonomy = () => {
    setTimeout(() => {
      this.handleModalOpen();
    }, 3000);
  }
  render() {
    const { classes } = this.props;

    return (
      <div>
        <Button variant="raised" onClick={this.startAutonomy} color="secondary">
          Start Autonomy
        </Button>
        <div>
          <Modal
            aria-labelledby="simple-modal-title"
            aria-describedby="simple-modal-description"
            open={this.state.open}
            onClose={this.handleModalClose}
          >
            <Grid
              container
              alignItems="center"
              justify="center"
            >
              <Grid item>
                <div className={classes.paper}>
                  <Grid
                    container
                    direction="column"
                    alignItems="center"
                    justify="center"
                  >
                    <Grid item >
                      <CheckCircleIcon className={classes.checkCircle} />
                    </Grid>

                    <Grid item>
                      <Typography variant="display1" id="simple-modal-description">
                        Successfully completed the autonomous task!
                      </Typography>
                    </Grid>

                    <Grid item>
                      <Button variant="raised" onClick={this.handleModalClose}>Dismiss</Button>
                    </Grid>
                  </Grid>
                </div>
              </Grid>
            </Grid>
          </Modal>
        </div>
      </div>
    );
  }
}

// We need an intermediary variable for handling the recursive nesting.
const StartAutonomyButtonWithStyles = withStyles(styles)(StartAutonomyButton);

export default StartAutonomyButtonWithStyles;
