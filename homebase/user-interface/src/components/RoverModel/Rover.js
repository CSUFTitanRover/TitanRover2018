// import React, { Component } from 'react';
// import * as THREE from 'three';
// import PropTypes from 'prop-types';
// import Joint from './joint';

// // TODO: Improve look of model

// // All units in INCHES
// const J1_YOFFSET = 3.55;
// const J1_OFFSET_TO_FRONT = 25;
// const J2_LENGTH = 30.5;
// const J3_LENGTH = 14.5; // This could be 17
// const J4_LENGTH = 14.66;

// // These are all estimates, but aren't necessary for IK
// const BASE_WIDTH = 24;
// const BASE_LENGTH = 60;
// const BASE_THICKNESS = 5;
// const WHEEL_OFFSET = 6;
// const WHEEL_RADIUS = 6;
// const WHEEL_THICKNESS = 3;

// export default class Rover extends Component {
//   constructor(props, context) {
//     super(props, context);

//     this.basePosition = new THREE.Vector3(0, -BASE_THICKNESS / 2, 0);
//     this.wheelPosition = [new THREE.Vector3(BASE_LENGTH / 2, -WHEEL_OFFSET, BASE_WIDTH / 2),
//       new THREE.Vector3(BASE_LENGTH / 2, -WHEEL_OFFSET, -BASE_WIDTH / 2),
//       new THREE.Vector3(-BASE_LENGTH / 2, -WHEEL_OFFSET, -BASE_WIDTH / 2),
//       new THREE.Vector3(-BASE_LENGTH / 2, -WHEEL_OFFSET, BASE_WIDTH / 2)];
//     this.wheelRotation = new THREE.Euler(Math.PI / 2, 0, 0);
//     this.j1Position = new THREE.Vector3(BASE_LENGTH / 2 - J1_OFFSET_TO_FRONT, J1_YOFFSET, 0);
//   }

//   render() {
//     return (<group>
//       <mesh position={this.basePosition}>
//         <boxGeometry width={BASE_LENGTH} height={BASE_THICKNESS} depth={BASE_WIDTH} />
//         <meshBasicMaterial color={0xffffff} wireframe />
//       </mesh>

//       {this.wheelPosition.map(position =>
//         (<mesh rotation={this.wheelRotation} position={position}>
//           <cylinderGeometry
//             radiusTop={WHEEL_RADIUS}
//             radiusBottom={WHEEL_RADIUS}
//             height={WHEEL_THICKNESS}
//             radialSegments={20}
//           />

//           <meshBasicMaterial color={0xffffff} wireframe />
//         </mesh>
//         ),
//       )}

//       <group
// position={this.j1Position}
// rotation={new THREE.Euler(0, Math.PI - this.props.j1, 0)}>
//         <Joint length={J2_LENGTH} rotation={Math.PI / 2 - this.props.j2}>
//           <Joint length={J3_LENGTH} color={0xff0000} rotation={this.props.j3}>
//             <Joint length={J4_LENGTH} color={0x00ffff} rotation={this.props.j4} />
//           </Joint>
//         </Joint>
//       </group>

//       <group
//         position={this.j1Position}
//         rotation={new THREE.Euler(0, Math.PI - this.props.realj1, 0)}
//       >
//         <mesh position={new THREE.Vector3(0, -J1_YOFFSET / 2, 0)}>
//           <cylinderGeometry
//             radiusTop={8}
//             radiusBottom={8}
//             height={J1_YOFFSET}
//             radialSegments={20}
//           />
//           <meshBasicMaterial color={0xffffff} />
//         </mesh>
//         <Joint length={J2_LENGTH} rotation={Math.PI / 2 - this.props.realj2} phantom>
//           <Joint length={J3_LENGTH} color={0xff0000} rotation={this.props.realj3} phantom>
//             <Joint length={J4_LENGTH} color={0x00ffff} rotation={this.props.realj4} phantom />
//           </Joint>
//         </Joint>
//       </group>
//     </group>);
//   }
// }

// Rover.propTypes = {
//   j1: PropTypes.number.isRequired,
//   j2: PropTypes.number.isRequired,
//   j3: PropTypes.number.isRequired,
//   j4: PropTypes.number.isRequired,
//   realj1: PropTypes.number.isRequired,
//   realj2: PropTypes.number.isRequired,
//   realj3: PropTypes.number.isRequired,
//   realj4: PropTypes.number.isRequired,
// };
