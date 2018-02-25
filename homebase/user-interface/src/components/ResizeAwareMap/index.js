import React, { PureComponent } from 'react';
import ResizeAware from 'react-resize-aware';
import appSettings from '../../app-settings.json';
import Map from '../Map/';

/** A regular map component that is responsive to width/height changes of it's parent
 * by using ResizeAware. ResizeAware passes in the width and height to the Map component.
 * It also passes in the local map tile server's map style.
*/
class ResizeAwareMap extends PureComponent {
  render() {
    return (
      <ResizeAware style={{ width: '100%', height: '100%' }}>
        <Map mapStyle={appSettings.map.style} />
      </ResizeAware>
    );
  }
}

export default ResizeAwareMap;
