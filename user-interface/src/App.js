import React, { Component } from 'react'
import Layout from './containers/Layout'
import Stopwatch from './components/Stopwatch'
import 'typeface-roboto'

export default class App extends Component {
  render() {
    return (
      <Layout>
        <Stopwatch />
      </Layout>
    )
  }
}
