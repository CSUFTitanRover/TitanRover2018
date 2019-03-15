// import React, { Component } from 'react';
// import * as THREE from 'three';
// import PropTypes from 'prop-types';

// // A Joint on the rover
// const J_RAD = 3.46 / 2;

// export default class Joint extends Component {
//   render() {
//     let radius = J_RAD;
//     if (this.props.phantom) {
//       radius /= 2;
//     }

//     const jointRotation = new THREE.Euler(0, 0, this.props.rotation);
//     const jointPosition = new THREE.Vector3(0, this.props.length / 2, 0);
//     const endPosition = new THREE.Vector3(0, this.props.length, 0);

//     return (
//       <group rotation={jointRotation}>
//         <mesh position={jointPosition}>
//           <cylinderGeometry
//             radiusTop={radius}
//             radiusBottom={radius}
//             height={this.props.length}
//             radialSegments={20}
//           />
//           <meshBasicMaterial
//             color={this.props.color}
//             opacity={this.props.phantom ? 0.5 : 1}
//             transparent={this.props.phantom}
//           />
//         </mesh>

//         <mesh>
//           <sphereGeometry radius={radius} widthSegments={20} heightSegments={20} />
//           <meshBasicMaterial
//             color={this.props.color}
//             opacity={this.props.phantom ? 0.5 : 1}
//             transparent={this.props.phantom}
//           />
//         </mesh>

//         <group position={endPosition}>
//           {this.props.children}
//         </group>
//       </group>
//     );
//   }
// }

// Joint.propTypes = {
//   rotation: PropTypes.number,
//   length: PropTypes.number.isRequired,
//   color: PropTypes.number,
//   phantom: PropTypes.bool,
//   children: PropTypes.children,
// };

// Joint.defaultProps = {
//   color: 0x00ff00,
//   rotation: 0,
//   phantom: false,
// };
