import React, { PureComponent } from 'react';
import Camera from './Camera';
import CameraSettingControls from './CameraSettingControls';

class CameraWrapper extends PureComponent {
  render() {
    return (
      <React.Fragment>
        <CameraSettingControls {...this.props} />
        <Camera {...this.props} />
      </React.Fragment>
    );
  }
}

export default CameraWrapper;
