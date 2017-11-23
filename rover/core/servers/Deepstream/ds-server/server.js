const DeepstreamServer = require('deepstream.io');
const MongoDBStorageConnector = require('deepstream.io-storage-mongodb');
const C = DeepstreamServer.constants;
/*
The server can take
1) a configuration file path
2) null to explicitly use defaults to be overriden by server.set()
3) left empty to load the base configuration from the config file located within the conf directory.
4) pass some options, missing options will be merged with the base configuration
*/
const server = new DeepstreamServer('./ds-rover-config.yml');

server.set('storage', new MongoDBStorageConnector({
  connectionString: 'mongodb://127.0.0.1:27017/deepstream',
  defaultCollection: 'deepstream_records',
  splitChar: '/'
}));

// start the server
server.start();