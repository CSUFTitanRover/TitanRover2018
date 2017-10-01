import React, { Component } from 'react'
import Layout from './containers/Layout'
import GoldenLayout from './containers/GoldenLayout'
import './App.css'

export default class App extends Component {
  render() {
    return (
      <Layout>
        <GoldenLayout />
      </Layout>
    )
  }
}
