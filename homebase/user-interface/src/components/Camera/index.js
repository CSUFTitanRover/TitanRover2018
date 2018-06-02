import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import CameraStream from '../CameraStream/';
import CameraSettings from '../CameraSettings';

/** The complete camera component composed of CameraSettings and CameraStream.
 * Any props passed to this component will get passed on to both CameraSettings and CameraStream.
 */
class Camera extends PureComponent {
  static propTypes = {
    /** The unique camera ID */
    cameraID: PropTypes.string.isRequired,
  }

  render() {
    return (
      <div>
        <CameraSettings {...this.props} />
        <CameraStream {...this.props} />
      </div>
    );
  }
}

export default Camera;
