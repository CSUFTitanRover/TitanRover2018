import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import registerServiceWorker from './registerServiceWorker'
// import GoldenLayout from 'golden-layout'
// import 'golden-layout/src/css/goldenlayout-base.css'
// import 'golden-layout/src/css/goldenlayout-dark-theme.css'

ReactDOM.render(<App />, document.getElementById('root'))
registerServiceWorker()

// TODO: finish Golden Layout setup
// create skeleton layout
// const glLayout = new GoldenLayout({
//     content: [{
//         type: 'row',
//         content:[{
//             type:'react-component',
//             component: 'app-component',
//             props: { label: 'A' }
//         },{
//             type: 'column',
//             content:[{
//                 type:'react-component',
//                 component: 'app-component',
//                 props: { label: 'B' }
//             },{
//                 type:'react-component',
//                 component: 'app-component',
//                 props: { label: 'C' }
//             }]
//         }]
//     }]
// })

// // register/associate react component with string id
// glLayout.registerComponent('app-component', App)

// //Once all components are registered, call
// glLayout.init()
