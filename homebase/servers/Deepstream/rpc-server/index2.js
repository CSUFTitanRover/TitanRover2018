const PromiseSocket = require('promise-socket')
const { getClient } = require('./deepstream');
const net = require('net');

const tcpEndpoint = {
  address: '192.168.1.120',
  port: 9090
};

async function main() {
  const socket = new net.Socket();
  const promiseSocket = new PromiseSocket(socket);
  const dsClient = await getClient();
  const tcpClient = await promiseSocket.connect();


  tcpClient.connect(endpoint.port, endpoint.address, () => {
    dsClient.rpc.provide('addCoordinate', (data, response) => {
      const computedData = `1,${data}`;

      // no nice way to handle tcp write errors
      tcpClient.write(computedData, () => {
        response.send(`Successfully added your coordinate for ${computedData}`);
      })
    })

    dsClient.rpc.provide('popCoordinate', (data, response) => {
      const computedData = `2`;

      // no nice way to handle tcp write errors
      tcpClient.write(computedData, () => {
        response.send(`Successfully deleted your coordinate`);
      })
    })


    dsClient.rpc.provide('deleteCoordinate', (data, response) => {
      const computedData = `2,${data}`;

      // no nice way to handle tcp write errors
      tcpClient.write(computedData, () => {
        response.send(`Successfully deleted your coordinate`);
      })
    })

    dsClient.rpc.provide('deleteAllCoordinates', (data, response) => {
      const computedData = `0`;

      // no nice way to handle tcp write errors
      tcpClient.write(computedData, () => {
        response.send(`Successfully deleted all the coordinates`);
      })
    })
  });
};

// run the main function
main();