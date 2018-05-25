import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Dialog from '@material-ui/core/Dialog';
import Slide from '@material-ui/core/Slide';


class AddWaypointsDialog extends Component {
  static propTypes = {
    isOpen: PropTypes.bool,
    onClose: PropTypes.func.isRequired,
  }

  static defaultProps = {
    isOpen: false,
  }

  handleClose = () => {
    const { onClose } = this.props;
    onClose();
  }

  transition = props => <Slide direction="up" {...props} />

  render() {
    const { isOpen } = this.props;

    return (
      <Dialog
        fullScreen
        open={isOpen}
        onClose={this.handleClose}
        TransitionComponent={this.transition}
      >
        <div>hi</div>
      </Dialog>
    );
  }
}

export default AddWaypointsDialog;
