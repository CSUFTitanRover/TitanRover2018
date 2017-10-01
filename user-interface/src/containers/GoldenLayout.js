import React, { Component } from 'react'
import * as GL from 'golden-layout'
import Counter from '../components/Counter'

const config = {
  content: [
    {
      type: 'row',
      content: [
        {
          type: 'react-component',
          component: 'Counter'
        },
        {
          type: 'react-component',
          component: 'Counter'
        },
        {
          type: 'react-component',
          component: 'Counter'
        }
      ]
    }
  ]
}

export default class GoldenLayout extends React.Component {
  componentDidMount() {
    const layout = new GL(config, this.node)
    layout.registerComponent('Counter', Counter)
    layout.init()

    window.addEventListener('resize', () => layout.updateSize())
  }

  render() {
    return (
      <div
        className="goldenLayout"
        ref={node => {
          this.node = node
        }}
      />
    )
  }
}
