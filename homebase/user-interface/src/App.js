import React, { Component } from 'react';
import Reboot from 'material-ui/Reboot';
import Layout from './containers/Layout';
import GoldenLayout from './containers/GoldenLayout/';
import './App.css';

export default class App extends Component {
  render() {
    return (
      <React.Fragment>
        <Reboot />
        <Layout>
          <GoldenLayout />
        </Layout>
      </React.Fragment>
    );
  }
}
