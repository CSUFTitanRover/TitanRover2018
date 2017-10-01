import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import registerServiceWorker from './registerServiceWorker'

// adding this as a workaround for GL to work without ejecting CRA from the project
window.React = React
window.ReactDOM = ReactDOM

ReactDOM.render(<App />, document.getElementById('root'))
registerServiceWorker()
