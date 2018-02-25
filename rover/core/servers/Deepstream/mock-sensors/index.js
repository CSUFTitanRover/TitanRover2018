const yaml = require('js-yaml')
const fs = require('fs')
const chalk = require('chalk')
const argv = require('minimist')(process.argv.slice(2))
const { contains } = require('itertools')
const DefaultSensor = require('./src/DefaultSensor')
const CycleSensor = require('./src/CycleSensor')
const { clients } = require('./src/deepstream')
let { configFilePath } = require('./src/util')
const log = console.log;

try {
    let customConfigPath = argv.c || argv.config
    let mockConfig;

    if (customConfigPath) {
        log(`Using a custom config file: ${customConfigPath}`)
        log('Reading the mock config file...')
        mockConfig = yaml.safeLoad(fs.readFileSync(customConfigPath, 'utf8'))
        configFilePath = customConfigPath
    }
    else {
        log('Using the default config file: defaultMockConfig.yml')
        log('Reading the mock config file...')
        mockConfig = yaml.safeLoad(fs.readFileSync('./defaultMockConfig.yml', 'utf8'))
    }

    const sensors = Object.entries(mockConfig.sensors)
    log(chalk.green('Found the following sensor(s):'))

    sensors.forEach(([key, val]) => {
        log(chalk.yellow(key))

        const sensorProps = Object.keys(val)

        sensorProps.forEach(prop => {
            let isSettingsProp = contains(['timeDelay', 'debug', 'path', 'verbose', 'deepstreamServer', 'sensorType'], prop)

            if (!isSettingsProp) {
                log(chalk.cyan(`\t- ${prop}`))
            }
        })
    });

    log('\nMocking up sensors...')

    const mockedSensors = [];

    sensors.forEach(([key, val]) => {
        const { timeDelay, debug, path, verbose, deepstreamServer, sensorType } = val

        // get a new copy of the props
        // and delete the sensor settings
        const props = { ...val }
        delete props.path
        delete props.timeDelay
        delete props.debug
        delete props.verbose
        delete props.deepstreamServer
        delete props.sensorType

        let sensor;
        if (sensorType === 'default' || sensorType === undefined || sensorType === null) {
            sensor = new DefaultSensor(key, path, props, timeDelay, debug, verbose, deepstreamServer)
        }
        else if (sensorType === 'cycle') {
            sensor = new CycleSensor(key, path, props, timeDelay, debug, verbose, deepstreamServer)
        }

        mockedSensors.push(sensor)
    })

    log('Mocked up all of the sensors... starting them now.')

    mockedSensors.forEach(mockSensor => {
        mockSensor.start()
    })

    // setup a listener for ctrl-c
    process.on('SIGINT', () => {
        log("\nGracefully shutting down from  SIGINT (Crtl-C)")

        mockedSensors.forEach(mockSensor => {
            log(chalk.yellow(`Stopping ${mockSensor.name}...`))
            mockSensor.stop()
        })

        Object.entries(clients).forEach(([clientName, ds]) => {
            log(chalk.yellow(`Closing deepstream client connection to the ${clientName} deepstream server`))
            ds.close()
        })
        log(chalk.yellow("exiting..."))
        process.exit()
    })
}
catch (e) {
    console.error(e)
}
