import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { toast } from 'react-toastify';
import { getClient } from '../../utils/deepstream';

class Poker extends Component {
  state = { pokeLoading: false }

  async componentDidMount() {
    this.client = await getClient('homebase');
  }

  handlePoke = () => {
    this.setState({ pokeLoading: true });

    this.client.record.setData('rover/poke', { poke: true }, (err) => {
      if (err) {
        toast.error('There was an issue updating the poke record on deepstream.');
      }

      this.setState({ pokeLoading: false });
    });
  }

  render() {
    const { pokeLoading } = this.state;
    return (
      <Button fullWidth variant="raised" color="primary" onClick={this.handlePoke}>
        {pokeLoading ? <CircularProgress color="default" size={20} /> : 'Poke'}
      </Button>
    );
  }
}
export default (Poker);
