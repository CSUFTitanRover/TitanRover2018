/* For GPS coordinate formatting */
const DIRECTION_INDICATOR = ['S', '', 'N', 'W', '', 'E'];

export const convertToDegrees = coord => `${coord.toFixed(6)}°`;

export const convertToDMS = (coord) => {
  let remainder = Math.abs(coord);
  const degree = Math.floor(remainder);
  remainder -= degree;
  const min = Math.floor(remainder * 60);
  remainder -= min / 60;
  const sec = remainder * 3600;

  return `${degree}° ${min}' ${sec.toFixed(4)}"`;
};

export const formatCoordinate = (coord, vertical, dms) => {
  /* Test cases:
    (+, false): 1+1 = 2 = 'N'
    (0, false): 1+0 = 1 = ''
    (-, false): 1-1 = 0 = 'S'
    (+, true): 4+1 = 5 = 'E'
    (0, true): 4+0 = 4 = ''
    (-, true): 4-1 = 3 = 'W'
  */
  const useDms = dms || true;
  const direction = DIRECTION_INDICATOR[vertical * 3 + 1 + Math.sign(coord)];
  const num = useDms ? convertToDMS(coord) : convertToDegrees(coord);
  return `${num} ${direction}`;
};


export const convertDMSToDD = ({ degrees, minutes, seconds, direction }) => {
  const calculatedMinutes = Math.abs(parseFloat(minutes)) / 60;
  const calculatedSeconds = Math.abs(parseFloat(seconds)) / 3600;
  const result = Math.abs(parseFloat(degrees)) + calculatedMinutes + calculatedSeconds;

  // finally apply negative value depending on direction
  switch (direction.toLowerCase()) {
    case 'south':
    case 'west':
      return (result * -1);
    default:
      return result;
  }
};
