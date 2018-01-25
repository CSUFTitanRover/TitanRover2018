import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import appSettings from '../../app-settings.json';

class Camera extends PureComponent {
  static propTypes = {
    cameraID: PropTypes.string.isRequired,
    baseIP: PropTypes.string,
  }

  static defaultProps = {
    baseIP: appSettings.cameras.base_ip,
  }

  render() {
    const { baseIP, cameraID } = this.props;
    const port = `808${cameraID}`;
    return (
      <img src={`${baseIP}:${port}`} alt="camera" width={300} height={300} />
    );
  }
}

export default Camera;
