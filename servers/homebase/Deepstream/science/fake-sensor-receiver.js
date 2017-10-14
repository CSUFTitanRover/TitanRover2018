const { client } = require('./deepstream')

function start() {
  client.event.subscribe('science/decagon-5TE', payload => {
    console.log('--------')
    console.log('Received new payload...')
    console.log(payload)
  })
}

module.exports = {
  start
}
