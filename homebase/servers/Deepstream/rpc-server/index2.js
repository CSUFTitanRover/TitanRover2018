const PromiseSocket = require('promise-socket')
const { getClient } = require('./deepstream');
const { createDataString, getJointNameFromAddress, getSpeedNameFromValue } = require('./utils')
const {
  ADD_COORDINATE,
  DELETE_ALL_COORDINATES,
  DELETE_COORDINATE,
  POP_COORDINATE
} = require('./constants');

const tcpEndpoint = {
  host: 'localhost',
  port: 9999
};

async function main() {
  const tcpClient = new PromiseSocket();
  const dsClient = await getClient();
  await tcpClient.connect(tcpEndpoint);

  // hook up rpc providers for deepstream
  dsClient.rpc.provide('addCoordinate', async (data, response) => {
    try {
      const formattedData = createDataString(ADD_COORDINATE, data);
      console.log(`addCoordinate - formattedData: ${formattedData}`);
      const totalBytesSent = await tcpClient.write(formattedData)
      response.send(`Successfully added your coordinate for: ${formattedData}`);
    }
    catch (err) {
      response.error(err.toString())
    }
  });

  dsClient.rpc.provide('popCoordinate', async (data, response) => {
    try {
      const formattedData = createDataString(POP_COORDINATE, data);
      console.log(`popCoordinate - formattedData: ${formattedData}`);
      const totalBytesSent = await tcpClient.write(formattedData)
      response.send(`Successfully popped off the top coordinate for: ${formattedData}`);
    }
    catch (err) {
      response.error(err.toString())
    }
  });

  dsClient.rpc.provide('deleteCoordinate', async (data, response) => {
    try {
      const formattedData = createDataString(DELETE_COORDINATE, data);
      console.log(`deleteCoordinate - formattedData: ${formattedData}`);
      const totalBytesSent = await tcpClient.write(formattedData)
      response.send(`Successfully deleted your coordinate for: ${formattedData}`);
    }
    catch (err) {
      response.error(err.toString())
    }
  });

  dsClient.rpc.provide('deleteAllCoordinates', async (data, response) => {
    try {
      const formattedData = createDataString(DELETE_ALL_COORDINATES, data);
      console.log(`deleteAllCoordinates - formattedData: ${formattedData}`);
      const totalBytesSent = await tcpClient.write(formattedData)
      response.send(`Successfully deleted all the coordinates.`);
    }
    catch (err) {
      response.error(err.toString())
    }
  });

  dsClient.rpc.provide('changeMotorSpeed', async (data, response) => {
    try {
      const { address, value } = data;
      const formattedData = createDataString(address, value);
      console.log(`changeMotorSpeed - formattedData: ${formattedData}`);

      const totalBytesSent = await tcpClient.write(formattedData)
      const jointName = getJointNameFromAddress(address);
      const speedName = getSpeedNameFromValue(value);
      response.send(`Successfully changed the motor of ${jointName} to ${speedName}.`);
    }
    catch (err) {
      response.error(err.toString())
    }
  });
};

// run the main function
main();