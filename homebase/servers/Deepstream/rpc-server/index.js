const PromiseSocket = require('promise-socket')
const { getClient } = require('./deepstream');
const net = require('net');

const endpoint = {
    address: '192.168.1.120',
    port: 9090
};

async function main() {
    const tcpClient = new net.Socket();
    const dsClient = await getClient();

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