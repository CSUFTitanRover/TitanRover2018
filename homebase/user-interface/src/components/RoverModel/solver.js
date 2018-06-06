const length1 = 30.5;
const length2 = 14.5; // This could be 17
const length3 = 14.66;

const theta1LowerBound = -15 * Math.PI / 180;
const theta1UpperBound = 75 * Math.PI / 180;
const theta2LowerBound = 0 * Math.PI / 180;
const theta2UpperBound = 90 * Math.PI / 180;
const theta3LowerBound = -90 * Math.PI / 180;
const theta3UpperBound = 90 * Math.PI / 180;

const thetastep = 0.002;
const errorTolerance = 0.01;

let x = 0;
let y = 0;
let z = 0;

let j1 = 0;
let j2 = 0;
let j3 = 0;
let j4 = 0;

function xarm(jointNumber, theta0, theta1, theta2, theta3) {
  return (jointNumber * Math.cos(theta1 - theta2 + theta3) * Math.cos(theta0));
}

function yarm(jointNumber, theta0, theta1, theta2, theta3) {
  return (jointNumber * Math.cos(theta1 - theta2 + theta3) * Math.sin(theta0));
}

function zarm(jointNumber, theta1, theta2, theta3) {
  return (jointNumber * Math.sin(theta1 - theta2 + theta3));
}

function azimuthalcalculation() {
  if (x === 0 && y !== 0) {
    j1 = Math.arcsin(y / 1);
  } else if (x < 0) {
    j1 = Math.atan(y / x) + Math.PI;
  } else {
    j1 = Math.atan(y / x);
  }

  if (j1 > Math.PI) {
    j1 -= Math.PI * 2;
  }

  if (j1 < -Math.PI) {
    j1 += Math.PI * 2;
  }

  return j1;
}

function getDistance() {
  const xPosition1 = xarm(length1, j1, j2, 0, 0);
  const xPosition2 = xarm(length2, j1, j2, j3, 0);
  const xPosition3 = xarm(length3, j1, j2, j3, j4);

  const yPosition1 = yarm(length1, j1, j2, 0, 0);
  const yPosition2 = yarm(length2, j1, j2, j3, 0);
  const yPosition3 = yarm(length3, j1, j2, j3, j4);

  const zPosition1 = zarm(length1, j2, 0, 0);
  const zPosition2 = zarm(length2, j2, j3, 0);
  const zPosition3 = zarm(length3, j2, j3, j4);

  const xcurrent = xPosition1 + xPosition2 + xPosition3;
  const ycurrent = yPosition1 + yPosition2 + yPosition3;
  const zcurrent = zPosition1 + zPosition2 + zPosition3;

  const distance = Math.sqrt((xcurrent - x) ** 2 + (ycurrent - y) ** 2 + (zcurrent - z) ** 2);
  return distance;
}

function calculateNextStep(theta1step, theta2step, theta3step, distance) {
  let newDistance = distance;
  const theta1test = j2 + theta1step;
  const theta2test = j3 + theta2step;
  const theta3test = j4 + theta3step;

  const xtest = xarm(length1, j1, theta1test, 0, 0) +
    xarm(length2, j1, theta1test, theta2test, 0) +
    xarm(length3, j1, theta1test, theta2test, theta3test);
  const ytest = yarm(length1, j1, theta1test, 0, 0) +
    yarm(length2, j1, theta1test, theta2test, 0) +
    yarm(length3, j1, theta1test, theta2test, theta3test);
  const ztest = zarm(length1, theta1test, 0, 0) +
    zarm(length2, theta1test, theta2test, 0) +
    zarm(length3, theta1test, theta2test, theta3test);

  const distancetest = Math.sqrt((xtest - x) ** 2 + (ytest - y) ** 2 + (ztest - z) ** 2);

  if (distancetest < newDistance &&
    theta1LowerBound <= theta1test &&
    theta1test <= theta1UpperBound &&
    theta2LowerBound <= theta2test &&
    theta2test <= theta2UpperBound &&
    theta3LowerBound <= theta3test &&
    theta3test <= theta3UpperBound) {
    newDistance = distancetest;

    j2 = theta1test;
    j3 = theta2test;
    j4 = theta3test;
  }

  return newDistance;
}

export default function solve(target, t1, t2, t3, t4) {
  x = target.x;
  y = target.z;
  z = target.y;
  j1 = t1;
  j2 = t2;
  j3 = t3;
  j4 = t4;

  azimuthalcalculation();
  let distance = getDistance();

  let iterations = 0;
  let lastDistance = 0;
  while (distance > errorTolerance && iterations < 10000 && lastDistance !== distance) {
    lastDistance = distance;
    for (let i = -1; i <= 1; i += 1) {
      for (let j = -1; j <= 1; j += 1) {
        for (let k = -1; k <= 1; k += 1) {
          distance = calculateNextStep(i * thetastep, j * thetastep, k * thetastep, distance);
        }
      }
    }

    iterations += 1;
  }
  return [j1, j2, j3, -j4];
}

