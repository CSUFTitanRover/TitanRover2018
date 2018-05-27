import React, { PureComponent } from 'react';
import Camera from '../Camera/';

class StereoCamera extends PureComponent {
  render() {
    return (
      <Camera {...this.props} initialWidth={1344} initialHeight={376} />
    );
  }
}

export default StereoCamera;
