const PromiseSocket = require('promise-socket')
const { getClient } = require('./deepstream');
const net = require('net');



async function main() {
    const tcpClient = new net.Socket();
    const dsClient = await getClient();

    tcpClient.connect(9090, '192.168.1.120', () => {
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
            // const computedData = `2,${data}`;
            const computedData = `2,789,456`;
            
            
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