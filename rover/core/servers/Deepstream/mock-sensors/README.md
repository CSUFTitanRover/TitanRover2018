# Mock Sensors for Rover Deepstream Server

This serves as a testing platform for mocking sensors and emitting fake data to the deepstream server on the rover. You can easily have data pumped into the deepstream server for the homebase as well just by changing the port numbers.

## Getting Started

The settings for where to configure the fake sensors can be found in: `mockConfig.yml`

There are two required fields that need to be inside the config file: `deepstream` and `sensors`

### Deepstream

You must supply the deepstream endpoints where the mock sensors will push their data to. For now, only the websocket endpoint is used.

### Sensors

You can specify as many sensors with as many keys you want to be mocked in the config file!

For each sensor there are some required and optional fields to specify.

#### Sensor Fields

- `path`: This is the path where the data is emitted to on deepstream
- `timeDelay`: The delay between every emitted data point. Default is 1000 ms.
- `debug`: Turns on printing output to the console. Default is false.
- `verbose`: If debug is true, this option pretty prints the entire data payload to the console. Default is false.
- `<keyName>`: This is a key name that can be called whatever you want it to be. There can be as many keyNames as you want
    - `min`: The minimum value generated
    - `max`: The maximum value generated
    - `floatingPoint`: Generates the data value as a decimal or whole number.

## Example Config

```yml
# the deepstream endpoints the mock-sensors will use to pump data into
deepstream:
    websocket: localhost:3020
    http: localhost:3080 # currently is not used by any mocked sensor

# the sensors which will be mocked and
# how the fake data will look
sensors:
    Decagon-5TE:
        path: science/decagon # the path where the data is pushed into deepstream e.g science/decagon
        timeDelay: 1500 # [optional] [default = 1000] the amount of wait time in ms before emitting
        debug: false # [optional] [default = false] outputs generated data to the console
        verbose: false # [optional] [default = false] if debug is true, this prints out the raw data generated
        ec: 
            min: 0.85 # the min number the generated value will be 
            max: 1.1 # the max number the generated value will be 
            floatingPoint: true # controls if it's generated as a floating number
        humidity:
            min: 45
            max: 50
            floatingPoint: true
        temperature:
            min: 13
            max: 18.5
            floatingPoint: true
    Atmospheric:
        path: science/atmospheric
        timeDelay: 2500
        windspeed: 
            min: 3
            max: 6
            floatingPoint: false
        barometer:
            min: 28
            max: 32.25
            floatingPoint: true
        uvIndex:
            min: 0.9
            max: 1.1
            floatingPoint: true
            

```