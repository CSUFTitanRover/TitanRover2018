import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

import Button from 'material-ui/Button';
import Select from 'material-ui/Select';
import { MenuItem } from 'material-ui/Menu';

import c3 from 'c3';

const chartTypes = ['line', 'bar', 'spline'];

/* TODO:
Make the chart more data-relevant
    x-axis: time
    y-axis: labelled with units
Adjust margins and widths
Scroll the data points in a smarter way
Add different chart types
*/

export default class Chart extends Component {
  state = { active: true, chartType: this.props.chartType }

  // Create the C3 chart after mount
  componentDidMount() {
    // Generate the chart
    this.chart = c3.generate({
      bindto: '#titanChart',
      data: {
        json: [this.props.data],
        keys: { value: ['humidity', 'temperature', 'ec'] },
      },
    });
  }

  // If the props are changed, update the C3 chart
  componentWillReceiveProps(newProps) {
    // Return if real-time data is inactive
    if (!this.state.active) {
      return;
    }

    this.scrollPos += 1;
    this.chart.flow({ json: [newProps.data], keys: { value: ['humidity', 'temperature', 'ec'] }, duration: 500, to: this.scrollPos });
  }

  scrollPos = -this.props.maxPoints;
  chart = null
  dataPoints = 0

  // Enable/disable real-time data
  handleClick = () => {
    this.setState({
      active: !this.state.active,
    });
  }

  // Change chart type when a different chart is selected
  handleSelect = (e) => {
    const type = e.target.value;

    this.setState({
      chartType: type,
    });

    this.chart.transform(type);
  }

  render() {
    return (
      <Paper style={{ backgroundColor: '#FFFADD' }}>
        <Grid container>
          {/* Left side - options pane */}
          <Grid
            item
            xs
            container
            direction={'column'}
            align={'center'}
            justify={'center'}
            className={'MuiPaper-shadow2-5'}
            style={{ margin: '16px', backgroundColor: '#fff' }}
          >
            {/* Options pane title */}
            <Grid item style={{ marginBottom: '50%' }}>
              <Typography type={'title'}>Chart Options</Typography>
            </Grid>

            {/* Real-time data button */}
            <Grid item>
              <Button
                raised
                onClick={this.handleClick}
                color={this.state.active ? 'primary' : 'default'}
              >
                {this.state.active ? 'Listening' : 'Not listening'}
              </Button>
            </Grid>

            {/* Drop down menu */}
            <Grid item>
              <Select value={this.state.chartType} onChange={this.handleSelect}>
                {chartTypes.map(type =>
                  <MenuItem value={type} key={type}>{type}</MenuItem>,
                )}
              </Select>
            </Grid>
          </Grid>

          {/* Right side - chart */}
          <Grid item xs={10} container direction={'column'} align={'center'}>
            {/* Chart title */}
            <Grid item>
              <div><Typography type={'headline'}>{this.props.chartName}</Typography></div>
            </Grid>

            {/* The chart */}
            <Grid item style={{ width: '100%' }}>
              <div id="titanChart" />
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}

// Validation
Chart.propTypes = {
  chartName: PropTypes.string.isRequired,
  chartType: PropTypes.string,
  maxPoints: PropTypes.number.isRequired,
  data: PropTypes.arrayOf(PropTypes.object),
};

Chart.defaultProps = {
  chartType: 'line',
  data: [{}],
};
