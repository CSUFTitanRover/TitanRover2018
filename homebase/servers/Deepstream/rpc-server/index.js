const PromiseSocket = require('promise-socket')
const { getClient } = require('./deepstream');

function getTCPClient() {
    return new Promise(resolve => {})
}

async function main() {
    const promiseSocket = new PromiseSocket();
    const dsClient = await getClient();
    // const tcpClient = await promiseSocket.connect({host: '192.168.1.2', port: '80'});
    const tcpClient = {write: (data) => Promise.resolve()}

    dsClient.rpc.provide('addCoordinate', (data, response) => {
        tcpClient.write(data)
            .then(() => {;
                // finally tell them it succeeded
                response.send(`Successfully added your coordinate for ${data}`);
            })
            .catch(() => {
                response.error('Error: There was an issue adding the coordinate to the stack.')
            })
    })

};

// run the main function
main();