import React, { Component } from 'react';
import React3 from 'react-three-renderer';
import * as THREE from 'three';
import PropTypes from 'prop-types';
import Rover from './Rover';

export default class Thing extends Component {
  constructor(props, context) {
    super(props, context);

    this.cameraAngle = 0;
    this.cameraRef = undefined;
    this.lastMouseX = -1;
    this.lastShiftKey = false;

    // These need to be in state to trigger a re-render
    this.state = {
      pickResult: new THREE.Vector3(),
      cameraPosition: new THREE.Vector3(),
    };
  }

  _setCameraRef = (ref) => {
    this.cameraRef = ref;
  };

  handleLeftClick = (x, y) => {
    // Create a raycaster using the normalized mouse coordinates
    const origin = new THREE.Vector3(60 / 2 - 21, 3.55, 0); // Base plate origin
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2(x, y);
    const newPoint = new THREE.Vector3();
    raycaster.setFromCamera(mouse, this.cameraRef);

    if (this.lastShiftKey) {
      // Try to select a point on the plane of the arm if shift is held
      // FIXME: This isn't quite right, it seems a bit off...
      const angle = this.props.j1;
      const plane = new THREE.Plane();
      const normal = new THREE.Vector3(Math.sin(-angle), 0, Math.cos(-angle));
      plane.setFromNormalAndCoplanarPoint(normal, origin);

      raycaster.ray.intersectPlane(plane, newPoint);
    } else {
      // Just select the closest point on the ray to the picked position
      raycaster.ray.closestPointToPoint(this.state.pickResult, newPoint)
    }

    this.setState({ pickResult: newPoint });
    if (this.props.handlePickCallback) {
      this.props.handlePickCallback(newPoint.clone().sub(origin));
    }
  }

  // Deal with mouse dragging
  onDrag = (e) => {
    e.preventDefault();

    if (e.buttons === 4 || (e.buttons === 2 && e.ctrlKey)) { // Middle mouse button is down
      this.panCamera(Math.PI / 180 * (this.lastMouseX - e.nativeEvent.offsetX));
    } else if (e.buttons === 2) { // Right mouse button
      const change = -Math.PI / 180 * (this.lastMouseX - e.nativeEvent.offsetX);

      if (this.props.handleRotation) {
        this.props.handleRotation(change);
      }
    } else if (e.buttons === 1) { // Left mouse down
      const normX = e.nativeEvent.offsetX / e.target.width * 2 - 1;
      const normY = -e.nativeEvent.offsetY / e.target.height * 2 + 1;
      this.handleLeftClick(normX, normY);
    }

    // Shift view when holding tab down to more easily align point
    if (e.shiftKey !== this.lastShiftKey) {
      this.panCamera(0, e.shiftKey);
      this.lastShiftKey = e.shiftKey;
    }

    this.lastMouseX = e.nativeEvent.offsetX;
  }

  startDrag = (e) => {
    e.preventDefault();

    if (e.buttons === 2 || e.buttons === 4) { // Right or middle mouse button is down
      this.lastMouseX = e.nativeEvent.offsetX;
    } else if (e.buttons === 1) { // Left mouse down
      const normX = e.nativeEvent.offsetX / e.target.width * 2 - 1;
      const normY = -e.nativeEvent.offsetY / e.target.height * 2 + 1;
      this.handleLeftClick(normX, normY);
    }
  }

  // Handle camera movement
  panCamera = (amount, type) => {
    // Pan camera around the origin, and rerender
    this.cameraAngle += amount;
    let angle = this.cameraAngle;
    if (type) {
      angle = this.props.j1;
    }

    const cameraPosition = new THREE.Vector3(
      100 * Math.sin(-angle),
      type ? 0 : 60, 100 * Math.cos(-angle));

    // Update camera state and look at the center
    this.setState({ cameraPosition }, () => {
      this.cameraRef.lookAt(new THREE.Vector3(0, 0, 0));
    });
  }

  // Place camera after ref is created
  componentDidMount() {
    this.panCamera(Math.PI / 2);
  }

  render() {
    return (<div
      role="presentation"
      style={{ display: 'inline-block' }}
      onMouseMove={this.onDrag}
      onMouseDown={this.startDrag}
      onContextMenu={(e) => { e.preventDefault(); }}
    >

      <React3
        mainCamera="camera"
        width={this.props.width}
        height={this.props.height}
      >
        <scene>
          <perspectiveCamera
            name="camera"
            fov={60}
            aspect={this.props.width / this.props.height}
            near={0.1}
            far={1000}
            ref={this._setCameraRef}

            position={this.state.cameraPosition}
          />

          <group>
            <Rover
              j1={this.props.j1}
              j2={this.props.j2}
              j3={this.props.j3}
              j4={this.props.j4}
              realj1={this.props.realj1}
              realj2={this.props.realj2}
              realj3={this.props.realj3}
              realj4={this.props.realj4}
            />

            {/* Pick sphere to see where you clicked */}
            <group>
              <mesh position={this.state.pickResult}>
                <sphereGeometry radius={1} />
                <meshBasicMaterial color={0x888888} />
              </mesh>
            </group>
          </group>
        </scene>
      </React3>
    </div>);
  }
}

Thing.propTypes = {
  width: PropTypes.number,
  height: PropTypes.number,
  j1: PropTypes.number.isRequired,
  j2: PropTypes.number.isRequired,
  j3: PropTypes.number.isRequired,
  j4: PropTypes.number.isRequired,
  realj1: PropTypes.number.isRequired,
  realj2: PropTypes.number.isRequired,
  realj3: PropTypes.number.isRequired,
  realj4: PropTypes.number.isRequired,
  handleRotation: PropTypes.func,
  handlePickCallback: PropTypes.func,
};

Thing.defaultProps = {
  width: 400,
  height: 400,
  handleRotation: null,
  handlePickCallback: null,
};
