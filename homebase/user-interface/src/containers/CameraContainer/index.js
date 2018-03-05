import React, { PureComponent } from 'react';
import Camera from '../../components/CameraStream/';
import CameraSettingControls from '../../components/CameraSettings';
import appSettings from '../../app-settings.json'
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
