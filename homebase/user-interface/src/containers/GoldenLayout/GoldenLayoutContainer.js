import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

const propTypes = {
  Playground: PropTypes.node.isRequired,
};

const mapStateToProps = state => ({ Playground: state.playground });

class GoldenLayoutContainer extends Component {
  render() {
    const { Playground } = this.props;

    if (!Playground) {
      return null;
    }

    return (
      <Playground />
    );
  }
}

GoldenLayoutContainer.propTypes = propTypes;

export default connect(mapStateToProps)(GoldenLayoutContainer);

