const deepstream = require('deepstream.io-client-js')
const roverSettings = require('./roverSettings.json')

const { serverAddress } = roverSettings.deepstream

const client = deepstream(serverAddress.wss)
const mobilityRecord = client.record.getRecord('rover/mobility')
const sensorsRecord = client.record.getRecord('rover/sensors')
const diagnosticsRecord = client.record.getRecord('rover/diagnostics')

module.exports = {
  DEEPSTREAM_ADDRESS_WSS: serverAddress.wss,
  client,
  mobilityRecord,
  sensorsRecord,
  diagnosticsRecord
}
