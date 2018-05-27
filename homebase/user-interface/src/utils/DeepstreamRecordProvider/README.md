Using a single record path:

```js
function handleNewPayload(payload, recordName) {
  console.log(`New payload received on ${recordName}`);
  console.log(JSON.stringify(payload, null, 4));
}

<DeepstreamRecordProvider recordPath="rover/reach" onNewPayload={handleNewPayload}>
  {({subscribed, subscribeToUpdates, unsubscribeToUpdates}) => (
    <div>
      <h1>This component's subscription is currently: {subscribed.toString()}</h1>

      <button onClick={subscribeToUpdates}>Subscribe to Updates</button>
      <hr />
      <button onClick={unsubscribeToUpdates}>Unsubscribe to Updates</button>
    </div>
  )}
</DeepstreamRecordProvider>
```


Using multiple record paths:

```js
function handleNewPayload(payload, recordName) {
  console.log(`New payload received on ${recordName}`);
  console.log(JSON.stringify(payload, null, 4));
}

<DeepstreamRecordProvider recordPath={['rover/reach', 'rover/imu']} onNewPayload={handleNewPayload}>
  {({subscribed, subscribeToUpdates, unsubscribeToUpdates}) => (
    <div>
      <h1>This component's subscription is currently: {subscribed.toString()}</h1>

      <button onClick={subscribeToUpdates}>Subscribe to Updates</button>
      <hr />
      <button onClick={unsubscribeToUpdates}>Unsubscribe to Updates</button>
    </div>
  )}
</DeepstreamRecordProvider>
```
