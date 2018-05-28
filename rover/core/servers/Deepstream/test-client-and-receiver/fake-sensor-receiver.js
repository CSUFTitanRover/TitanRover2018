const { getClient } = require('./deepstream');

async function start() {
  let client = await getClient();

  const decagonList = client.record.getList('science/decagon-5TE');

  decagonList.whenReady(list => {
    list.subscribe(entry => {
      console.log('--------');
      console.log('Received new a entry...');
      console.log(entry);
    });
  });
};

module.exports = {
  start
};