import React, { Component } from 'react'
//import Layout from './containers/Layout'
//import Stopwatch from './components/Stopwatch'
import Chart from './components/Chart'
import 'typeface-roboto'
import "c3/c3.css"

let testData = {
  sensor1: [
    {temp: 95, humidity: 80, ec: 50},
    {temp: 94, humidity: 81, ec: 48},
    {temp: 94, humidity: 82, ec: 70},
    {temp: 96, humidity: 80, ec: 55},
    {temp: 95, humidity: 80, ec: 40},
    {temp: 96, humidity: 81, ec: 60}
  ]
};



export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {data: testData};

    setInterval(this._testUpdate.bind(this), 2000);
  }

  _testUpdate() {
    testData = {sensor1: [{
      temp: Math.random() * 10 + 90, 
      humidity: Math.random() * 5 + 80, 
      ec: Math.random() * 20 + 60}]};
    this.setState({data: testData});
  }

  render() {
    return (
      <Chart data={this.state.data} chartName={"Test Chart 1"} sensorName={"sensor1"} maxPoints={8}/>
    )
  }
}
