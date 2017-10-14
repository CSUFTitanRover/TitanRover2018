const { client } = require('./deepstream')

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min)
  max = Math.floor(max)
  return Math.floor(Math.random() * (max - min + 1)) + min //The maximum is inclusive and the minimum is inclusive
}

function start() {
  setInterval(() => {
    let humidity = getRandomIntInclusive(5, 50)
    let temperature = getRandomIntInclusive(85, 102)
    let ec = getRandomIntInclusive(5, 20)
    let timestamp = new Date()

    let payload = {
      humidity,
      temperature,
      ec,
      timestamp
    }

    client.event.emit('science/decagon-5TE', JSON.stringify(payload))
  }, 1000)
}

module.exports = {
  start
}
