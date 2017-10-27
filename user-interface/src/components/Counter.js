import React, { Component } from 'react';

const styles = {
  marginTop: 20,
  padding: 5,
  color: 'white',
};

class Counter extends Component {
  constructor(props) {
    super(props);

    this.state = { value: 0 };
  }

  increment = () => {
    this.setState({ value: this.state.value + 1 });
  }

  incrementBy3Bad = () => {
    // this will not work as React batches updates into 1 single call to preserve efficiency
    this.setState({ value: this.state.value + 1 });
    this.setState({ value: this.state.value + 1 });
    this.setState({ value: this.state.value + 1 });
  }

  incrementBy3Good = () => {
    // using arrow functions (preferred)
    this.setState(prevState => ({ value: prevState.value + 1 }));
    this.setState(prevState => ({ value: prevState.value + 1 }));
    this.setState(prevState => ({ value: prevState.value + 1 }));
  }

  render() {
    const { value } = this.state;

    return (
      <div style={styles}>
        <div>Value: {value}</div>

        <button onClick={this.increment}>increment by 1</button>
        <button onClick={this.incrementBy3Bad}>increment by 3 (Bad)</button>
        <button onClick={this.incrementBy3Good}>increment by 3 (Good)</button>
      </div>
    );
  }
}

export default Counter;
