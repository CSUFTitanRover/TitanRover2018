var format = require('date-fns/format')
const { getRandomIntInclusive, getRandomFloatInclusive, nextCycleItem } = require('./util')
const { getClient } = require('./deepstream')
const { range, cycle } = require('itertools')
const chalk = require('chalk')
const log = console.log

class CycleSensor {
  constructor(name, path, props, timeDelay = 1000, debug = false, verbose = false, deepstreamServer = 'rover') {
    this.name = name
    this.path = path
    this.props = Object.entries(props)
    this.timeDelay = timeDelay
    this.debug = debug
    this.verbose = verbose
    this.deepstreamServer = deepstreamServer
    this._ds = null
    this._interval = null
    this._cycleIterators = {}

    this.start = this.start.bind(this)
    this.stop = this.stop.bind(this)
    this.emit = this.emit.bind(this)
    this.generateSensorCycles = this.generateSensorCycles.bind(this)

    this.generateSensorCycles();
  }

  generateSensorCycles() {
    this.props.forEach(([key, val]) => {
      // create the cycle list for each individual reading
      let cycleIterator = this._generateCycleIterator(val)
      this._cycleIterators[key] = cycleIterator
    })
  }

  async start() {
    try {
      this._ds = await getClient(this.deepstreamServer)

      let startMessage = `Starting ${this.name} sensor... `

      if (this.debug) {
        const debuggingType = this.verbose ? 'verbose debugging' : 'normal debugging'
        startMessage += `with ${chalk.underline.green(debuggingType)} turned on.`
      }

      log(chalk.green(startMessage))

      this._interval = setInterval(() => {
        this.emit();
      }, this.timeDelay)
    }
    catch (e) {
      console.error(e)
      process.exit(1)
    }
  }

  stop() {
    clearInterval(this._interval)
  }

  emit() {
    let timestamp = Date.now()
    let payload = { timestamp }

    // load data into the payload
    this.props.forEach(([key, _]) => {
      let data = nextCycleItem(this._cycleIterators[key])
      payload[key] = data

      if (this.debug) {
        log(chalk.yellow(`${format(timestamp, 'HH:mm:ss.SSS A')} - ${this.name} [${this.path}] - Generated value for ${key}: ${data}`))
      }
    })

    // Set data to record path
    this._ds.record.setData(this.path, payload)

    if (this.debug) {
      if (this.verbose) {
        log(chalk.cyan(JSON.stringify(payload, null, 4)))
      }
      log('---------------')
    }

  }

  _generateCycleIterator(p) {
    // if both min and max are negative
    // multiply by -1 against the step
    // to allow the range func to still work properly
    if (p.min < 0 && p.max < 0) {
      p.step *= -1
    }

    let head = [...range(p.min, p.max, p.step)]
    let tail = [...range(p.max, p.min, (p.step * -1))]
    let r = [...head, ...tail]
    return cycle(r)
  }
}

module.exports = CycleSensor