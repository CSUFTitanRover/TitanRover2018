import { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { getClient, getRecord } from '../../utils/deepstream';

/** A Higher Order Component that uses the renderProps technique to provide deepstream updates to
 * a child component.
 *
 * In order to use this HOC, provide a function as the child component.
 * There are 3 parameters that are then passed to the
 * function: subscribed, subscribeToUpdates, unsubscribeToUpdates
 *
 * @see Look at Map.js for a working example
 */
class DeepstreamRecordProvider extends PureComponent {
  static propTypes = {
    /** Can be a single or multiple record paths to subscribe to */
    recordPath: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.arrayOf(PropTypes.string)],
    ).isRequired,
    /** The children function is passed in params that can be used when rendering the child element.
     * @param {bool} subscribed - The state if the record(s) are subscribed to or not.
     * @param {function} subscribeToUpdates- A function that subscribes record(s) to updates.
     * @param {function} unsubscribeToUpdates - A function that unsubscribes record(s) from updates.
     */
    children: PropTypes.func.isRequired,
    /** Called every time when a record updates.
     * @param {any} payload - The updated data
     * @param {string} recordName - The name of the record that was updated.
     */
    onNewPayload: PropTypes.func,
    /** The type of deepstream client to use. Can be "rover" or "homebase". */
    clientType: PropTypes.string,
  }

  static defaultProps = {
    onNewPayload: null,
    clientType: 'homebase',
  }

  client = null;
  record = null;
  records = null; // used if multiple records are being subscribed to
  recordCallbacks = {}; // used for unsubscribing record's callbacks
  multipleRecords = false;
  state = {
    /** Determines if the record(s) is currently subscribed to. */
    subscribed: false,
  }

  async componentDidMount() {
    try {
      const { recordPath, clientType } = this.props;
      this.client = await getClient(clientType);

      if (typeof recordPath === 'string') {
        this.record = await getRecord(this.client, recordPath);
      } else if (recordPath instanceof Array) {
        this.records = [];
        this.multipleRecords = true;

        const resolvedRecords = await Promise.all(
          recordPath.map(path => getRecord(this.client, path)),
        );

        resolvedRecords.forEach((record) => {
          this.records.push(record);
        });
      }

      // automatically start subscribing to changes
      this.subscribeToUpdates();
    } catch (e) {
      console.error(e);
    }
  }

  _generateCallbackForNewPayload = recordName => (payload) => {
    const { onNewPayload } = this.props;

    if (onNewPayload !== null) {
      onNewPayload(payload, recordName);
    }
  };

  _subscribe = (record) => {
    const callback = this._generateCallbackForNewPayload(record.name);
    // add the generated callback by using its record name as
    // it's key for later usage when unsubscribing
    this.recordCallbacks[record.name] = callback;
    record.subscribe(callback, true);
  }

  _unsubscribe = (record) => {
    record.unsubscribe(this.recordCallbacks[record.name]);
    // remove the generated callback
    delete this.recordCallbacks[record.name];
  }

  subscribeToUpdates = () => {
    const { subscribed } = this.state;

    if (!subscribed) {
      this.setState({ subscribed: true });

      if (!this.multipleRecords) {
        this._subscribe(this.record);
      } else {
        this.records.forEach((record) => {
          this._subscribe(record);
        });
      }
    }
  }

  unsubscribeToUpdates = () => {
    const { subscribed } = this.state;

    if (subscribed) {
      this.setState({ subscribed: false });

      if (!this.multipleRecords) {
        this._unsubscribe(this.record);
      } else {
        this.records.forEach((record) => {
          this._unsubscribe(record);
        });
      }
    }
  }

  componentWillUnmount() {
    if (!this.multipleRecords) {
      this.record.discard();
    } else {
      this.records.forEach((record) => {
        record.discard();
      });
    }
  }

  render() {
    const { subscribed } = this.state;
    const { children } = this.props;

    return (
      children(subscribed, this.subscribeToUpdates, this.unsubscribeToUpdates)
    );
  }
}

export default DeepstreamRecordProvider;
