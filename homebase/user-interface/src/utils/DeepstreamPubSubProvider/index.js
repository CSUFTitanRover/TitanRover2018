import { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { getClient } from '../../utils/deepstream';

/** A Higher Order Component that uses the renderProps technique to provide deepstream updates to
 * a child component.
 *
 * In order to use this HOC, provide a function as the child component.
 * There are 3 parameters that are then passed to the
 * function: subscribed, subscribeToUpdates, unsubscribeToUpdates
 *
 * @see Look at RealtimeChart.js for a working example
 */
class DeepstreamPubSubProvider extends PureComponent {
  static propTypes = {
    /** Can be one single or multiple subscriptions paths to subscribe to. */
    eventName: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.arrayOf(PropTypes.string)],
    ).isRequired,
    /** The children function is passed in params that can be used when rendering the child element.
     * @param {bool} subscribed - The state if the record(s) are subscribed to or not.
     * @param {function} subscribeToUpdates - A function that subscribes record(s) to updates.
     * @param {function} unsubscribeToUpdates - A function that unsubscribes record(s) from updates.
     */
    children: PropTypes.func.isRequired,
    /** Called every time when an event updates.
     * @param {any} payload  - The updated data
     * @param {string} eventName - The name of the event that was updated.
     */
    onNewPayload: PropTypes.func,
    /** The type of deepstream client to use. Can be "rover" or "homebase". */
    clientType: PropTypes.string,
  }

  static defaultProps = {
    onNewPayload: null,
    clientType: 'rover',
  }

  client = null;
  eventCallbacks = {}; // used for unsubscribing event's callbacks
  multipleEvents = false;
  state = {
    /** Determines if the event(s) is currently subscribed to. */
    subscribed: false,
  }

  async componentDidMount() {
    try {
      this.client = await getClient(this.props.clientType);
      this.multipleEvents = (this.props.eventName instanceof Array);
      // automatically start subscribing to changes
      this.subscribeToUpdates();
    } catch (e) {
      console.error(e);
    }
  }

  _generateCallbackForNewPayload = eventName => (payload) => {
    const { onNewPayload } = this.props;

    if (onNewPayload !== null) {
      onNewPayload(payload, eventName);
    }
  }

  _subscribe = (eventName) => {
    const callback = this._generateCallbackForNewPayload(eventName);
    // add the generated callback by using its eventName as
    // it's key for later usage when unsubscribing
    this.eventCallbacks[eventName] = callback;
    this.client.event.subscribe(eventName, callback);
  }

  _unsubscribe = (eventName) => {
    this.client.event.unsubscribe(eventName, this.eventCallbacks[eventName]);
    // remove the generated callback
    delete this.eventCallbacks[eventName];
  }

  subscribeToUpdates = () => {
    const { subscribed } = this.state;
    const { eventName } = this.props;

    if (!subscribed) {
      if (!this.multipleEvents) {
        this._subscribe(eventName);
      } else {
        eventName.forEach((e) => {
          this._subscribe(e);
        });
      }

      this.setState({ subscribed: true });
    }
  }

  unsubscribeToUpdates = () => {
    const { subscribed } = this.state;
    const { eventName } = this.props;

    if (subscribed) {
      if (!this.multipleEvents) {
        this._unsubscribe(eventName);
      } else {
        eventName.forEach((e) => {
          this._unsubscribe(e);
        });
      }

      this.setState({ subscribed: false });
    }
  }

  componentWillUnmount() {
    this.unsubscribeToUpdates();
  }

  render() {
    const { subscribed } = this.state;
    const { children } = this.props;

    return (
      children(subscribed, this.subscribeToUpdates, this.unsubscribeToUpdates)
    );
  }
}

export default DeepstreamPubSubProvider;
