import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore } from 'redux';
import appStore from './reducers/';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

// adding this as a workaround for Golden-Layout to work without ejecting CRA from the project
window.React = React;
window.ReactDOM = ReactDOM;

// create store with appStore
// and add support for google chrome Redux extension
const store = createStore(
  appStore,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__(),
);

const AppWithProvider = (
  <Provider store={store}>
    <App />
  </Provider>
);

ReactDOM.render(AppWithProvider, document.getElementById('root'));
registerServiceWorker();
