import React, { PureComponent } from 'react';
import Camera from './Camera';
import CameraSettingControls from './CameraSettingControls';
import appSettings from '../../appSettings.json'
  ;

class CameraWrapper extends PureComponent {
  state = { baseIP: appSettings.cameras.base_ip }

  cameraWrapperBaseIPChange = (val) => { this.setState({ baseIP: val }); }

  render() {
    return (
      <React.Fragment>
        <CameraSettingControls
          {...this.props}
          cameraWrapperBaseIPChange={this.cameraWrapperBaseIPChange}
        />
        <Camera {...this.props} baseIP={this.state.baseIP} />
      </React.Fragment>
    );
  }
}

export default CameraWrapper;
