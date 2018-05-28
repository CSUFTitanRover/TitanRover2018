# Testing Deepstream

This directory contains some fake sensor emitter and receiver files to serve as testing purposes.

## Getting started

This will execute `main.js` and will display the results in the console from the receiver and also start emitting fake payloads.

1. `npm install`
2. `npm start`

## Fake Sensor Emitter

This sensor updates the record list named (case sensitive): `science/decagon-5TE/<UTC-Timestamp>`

Keep in mind that the path `science/decagon-5TE` refers to the record list of which the sensor data will be added into Deepstream via the UTC Timestamp (in milliseconds).

So for example:

```
science/decagon-5TE
    /1518288191
        humidity: 40,
        temperature: 95,
        ec: 7,
        timestamp: 1518288191
    /1518288209
        humidity: 25,
        temperature: 99,
        ec: 12,
        timestamp: 1518288209
...
```

With a fake payload in the following format: 
```js
{
    humidity: <int>,
    temperature: <int>,
    ec: <int>,
    timestamp: <UTC-Timestamp>
}
```

The payload is JSON stringified before being emitted to Deepstream. So I would advise calling `JSON.parse()` if you are receiving the payload in order to manipulate it.

----

References

- https://deepstreamhub.com/tutorials/guides/lists/
- https://deepstreamhub.com/docs/client-js/datasync-list/
