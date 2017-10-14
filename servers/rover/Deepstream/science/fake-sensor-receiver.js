const { getClient } = require('./deepstream')

async function start() {
  let client = await getClient();

  client.event.subscribe('science/decagon-5TE', payload => {
    console.log('--------')
    console.log('Received new payload...')
    console.log(payload)
  })
}

module.exports = {
  start
}


start();