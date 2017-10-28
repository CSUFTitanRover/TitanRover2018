# Science Sensors

This directory contains some fake sensor emitter and receiver files to serve as testing purposes.

## Getting started

This will execute `main.js` and will display the results in the console from the receiver and also start emitting fake payloads.

1. `npm install`
2. `npm start`

## Fake Sensor Emitter

This sensor emits an event named (case sensitive): `science/decagon-5TE`

With a fake payload in the following format: 
```js
{
    humidity: <int>,
    temperature: <int>,
    ec: <int>,
    timestamp: <DateTime>
}
```

The payload is JSON stringified before being emitted to Deepstream. So I would advise calling `JSON.parse()` if you are receiving the payload in order to manipulate it.


