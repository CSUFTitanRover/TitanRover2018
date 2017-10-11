const deepstream = require('deepstream.io-client-js');
const roverSettings = require('./roverSettings.json');

const { URI } = roverSettings.deepstream;

const client = deepstream(URI.ws).login();

client.on('error', (error, event, topic) => console.log(error, event, topic));

module.exports = {
  client,
};
