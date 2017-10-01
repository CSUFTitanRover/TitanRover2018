import React, { Component } from 'react';

const styles = {
  border: '1px solid black',
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

  incrementBy3_bad = () => {
    // this will not work as React batches updates into 1 single call to preserve efficiency
    this.setState({ value: this.state.value + 1 });
    this.setState({ value: this.state.value + 1 });
    this.setState({ value: this.state.value + 1 });
  }

  incrementBy3_good = () => {
    // using a normal function
    this.setState(prevState => ({ value: prevState.value + 1 }));
    this.setState(prevState => ({ value: prevState.value + 1 }));
    this.setState(prevState => ({ value: prevState.value + 1 }));

    // using arrow functions (preferred)
    // this.setState((prevState) => {
    //   return { value: prevState.value + 1 }
    // })
    // this.setState((prevState) => {
    //   return { value: prevState.value + 1 }
    // })
    // this.setState((prevState) => {
    //   return { value: prevState.value + 1 }
    // })
  }

  render() {
    const { name } = this.props;
    const { value } = this.state;

    return (
      <div style={styles}>
        <h2 style={{ color: 'blue' }}>{name}</h2>
        <div>Value: {value}</div>

        <button onClick={this.increment}>increment by 1</button>
        <button onClick={this.incrementBy3_bad}>increment by 3 (Bad)</button>
        <button onClick={this.incrementBy3_good}>increment by 3 (Good)</button>
      </div>
    );
  }
}

export default Counter;
