Using a single event:

```js
function handleNewPayload(payload, eventName) {
  console.log(`New payload received on ${eventName}`);
  console.log(JSON.stringify(payload, null, 4));
}

<DeepstreamPubSubProvider eventName="science/decagon" onNewPayload={handleNewPayload}>
  {({subscribed, subscribeToUpdates, unsubscribeToUpdates}) => (
    <div>
      <h1>This component's subscription is currently: {subscribed.toString()}</h1>

      <button onClick={subscribeToUpdates}>Subscribe to Updates</button>
      <hr />
      <button onClick={unsubscribeToUpdates}>Unsubscribe to Updates</button>
    </div>
  )}
</DeepstreamPubSubProvider>
```

Using multiple events:

```js
function handleNewPayload(payload, recordName) {
  console.log(`New payload received on ${recordName}`);
  console.log(JSON.stringify(payload, null, 4));
}

<DeepstreamPubSubProvider eventName={['science/decagon', 'science/atmospheric']} onNewPayload={handleNewPayload}>
  {({subscribed, subscribeToUpdates, unsubscribeToUpdates}) => (
    <div>
      <h1>This component's subscription is currently: {subscribed.toString()}</h1>

      <button onClick={subscribeToUpdates}>Subscribe to Updates</button>
      <hr />
      <button onClick={unsubscribeToUpdates}>Unsubscribe to Updates</button>
    </div>
  )}
</DeepstreamPubSubProvider>
```
