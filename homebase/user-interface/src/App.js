import React, { Component } from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Layout from './containers/Layout';
import GoldenLayout from './containers/GoldenLayout/';
import './App.css';

export default class App extends Component {
  render() {
    return (
      <div>
        <CssBaseline />
        <Layout>
          <GoldenLayout />
        </Layout>
      </div>
    );
  }
}
