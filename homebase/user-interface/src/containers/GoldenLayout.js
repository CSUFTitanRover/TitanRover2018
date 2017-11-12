import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import * as GL from 'golden-layout';
import Counter from '../components/Counter';
import { addGoldenLayoutToStore } from '../actions/';

const propTypes = {
  /** Adds golden-layout object to global redux store */
  handleAddGoldenLayoutToStore: PropTypes.func.isRequired,
};

const mapDispatchToProps = dispatch => ({
  handleAddGoldenLayoutToStore: (glLayout) => {
    dispatch(addGoldenLayoutToStore(glLayout));
  },
});

// define a basic GL config
const config = {
  content: [
    {
      type: 'row',
      content: [
        {
          type: 'react-component',
          component: 'Counter',
        },
        {
          type: 'react-component',
          component: 'Counter',
        },
        {
          type: 'react-component',
          component: 'Counter',
        },
      ],
    },
  ],
};

/**
 * This is the playground area that Golden-Layout takes control of
 * to render any react components.
 */
class GoldenLayout extends Component {
  componentDidMount() {
    const layout = new GL(config, this.node);
    layout.registerComponent('Counter', Counter);
    layout.init();

    // debuggin purposes
    window.GL = GL;
    window.layout = layout;
    window.glnode = this.node;

    window.addEventListener('resize', () => {
      layout.updateSize();
    });

    this.props.handleAddGoldenLayoutToStore(layout);
  }

  render() {
    return (
      <div
        className="goldenLayout"
        ref={(node) => {
          this.node = node;
        }}
      />
    );
  }
}

GoldenLayout.propTypes = propTypes;

export default connect(null, mapDispatchToProps)(GoldenLayout);
