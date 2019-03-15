import React, { PureComponent } from 'react';
import ResizeAware from 'react-resize-aware';
// import appSettings from '../../appSettings.json';
import Map from '../Map/';

/** A regular map component that is responsive to width/height changes of it's parent
 * by using ResizeAware. ResizeAware passes in the width and height to the Map component.
 * It also passes in the local map tile server's map style.
*/
class ResizeAwareMap extends PureComponent {
  render() {
    return (
      <ResizeAware style={{ width: '100%', height: '100%' }}>
        {({ width, height }) => (
          <Map
            // mapStyle={appSettings.map.style}
            width={width}
            height={height}
          />
        )}
      </ResizeAware>
    );
  }
}

export default ResizeAwareMap;
