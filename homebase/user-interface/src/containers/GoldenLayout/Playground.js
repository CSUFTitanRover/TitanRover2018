import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import GoldenLayout from 'golden-layout';
import { initializeGL } from './utils';
import { addPlaygroundToStore } from '../../actions/goldenLayout';
import defaultGLConfig from './default-gl-config';

const defaultProps = {
  config: defaultGLConfig,
};

const propTypes = {
  /** Adds golden-layout object to global redux store */
  handleAddPlaygroundToStore: PropTypes.func.isRequired,
  config: PropTypes.object,
};

const mapDispatchToProps = dispatch => ({
  handleAddPlaygroundToStore: (glNode) => {
    dispatch(addPlaygroundToStore(glNode));
  },
});


/**
 * This is the playground area that Golden-Layout takes control of
 * to render any react components.
 */
class Playground extends Component {
  componentDidMount() {
    setTimeout(() => {
      const { config } = this.props;
      const glNode = new GoldenLayout(config, this.node);
      initializeGL(glNode);
      this.props.handleAddPlaygroundToStore(glNode);
    }, 150);
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

Playground.defaultProps = defaultProps;
Playground.propTypes = propTypes;

export default connect(null, mapDispatchToProps)(Playground);
