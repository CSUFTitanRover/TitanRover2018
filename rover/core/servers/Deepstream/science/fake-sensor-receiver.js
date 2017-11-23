const { getClient } = require('./deepstream');

async function start() {
  let client = await getClient();

  client.record.getRecord('decagon-5TE').whenReady(record => {
    record.subscribe(payload => {
      console.log('--------');
      console.log('Received new payload...');
      console.log(payload);
    });
  });
};

module.exports = {
  start
};