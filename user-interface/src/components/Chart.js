import React, { Component } from 'react';

import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

import Button from 'material-ui/Button';
import Select from 'material-ui/Select';
import { MenuItem } from 'material-ui/Menu';

var c3 = require("c3");

const chartTypes = ["line", "bar", "spline"];

/* TODO:
Make the chart more data-relevant 
    x-axis: time
    y-axis: labelled with units
Adjust margins and widths
Scroll the data points in a smarter way
Add different chart types
*/

export default class Chart extends Component {
    constructor(props) {
        super(props);

        // Initialize fields
        this.state = {active: true, chartType: this.props.chartType || "line"};
        this.chart = null;
        this.dataPoints = 0;
    }

    // Create the C3 chart after mount
    componentDidMount() {
        // Format data
        let data = this._formatData(this.props.data);
        this.dataPoints += data[0].length-1;

        // Generate the chart
        this.chart = c3.generate({
            bindto: "#titanChart",
            data: {
                columns: data
            }
        })
    }

    // If the props are changed, update the C3 chart
    componentWillReceiveProps(newProps) {
        // Return if real-time data is inactive
        if (!this.state.active) {
            return;
        }

        // Format data, then see how much to scroll by
        let tempData = this._formatData(newProps.data);
        this.dataPoints += tempData[0].length-1;
        let scrollPos = this.dataPoints - this.props.maxPoints;

        // Add the data and scroll
        this.chart.flow({columns: tempData, duration: 500, to: scrollPos});
    }

    // Takes the current props and transforms them to the C3 data format
    _formatData(data) {
        let sensorData = data[this.props.sensorName];
        let tempData = {};

        // Iterate through all the data points
        for (let i = 0; i < sensorData.length; i++) {
            for (let key in sensorData[i]) {
                if (!(key in tempData)) {
                    tempData[key] = [];
                }

                tempData[key].push(sensorData[i][key]);
            }
        }

        // Create new chart data
        let newChartData = [];
        for (let key in tempData) {
            newChartData.push([key].concat(tempData[key]));
        }

        return newChartData;
    }

    // Enable/disable real-time data
    handleClick() {
        this.setState({
            active: !this.state.active
        })
    }

    // Change chart type when a different chart is selected
    handleSelect(type) {
        this.setState({
            chartType: type
        })

        this.chart.transform(type);
    }

    render() {
        return (
            <Paper style={{backgroundColor: "#FFFADD"}}>
                <Grid container>
                    {/* Left side - options pane */}
                    <Grid item xs container direction={"column"} align={"center"} justify={"center"}
                        className={"MuiPaper-shadow2-5"} style={{margin: "16px", backgroundColor: "#fff"}}>
                        {/* Options pane title */}
                        <Grid item style={{marginBottom: "50%"}}>
                            <Typography type={"title"}>Chart Options</Typography>
                        </Grid>

                        {/* Real-time data button */}
                        <Grid item>
                            <Button raised onClick={() => this.handleClick()}
                                color={this.state.active ? "primary" : "default"}>
                                {this.state.active ? "Listening" : "Not listening"}
                            </Button>
                        </Grid>

                        {/* Drop down menu */}
                        <Grid item>
                            <Select value={this.state.chartType} onChange={(e) => this.handleSelect(e.target.value)}>
                                {chartTypes.map((type) =>
                                    <MenuItem value={type} key={type}>{type}</MenuItem>
                                )}
                            </Select>
                        </Grid>
                    </Grid>

                    {/* Right side - chart */}
                    <Grid item xs={10} container direction={"column"} align={"center"}>
                        {/* Chart title */}
                        <Grid item>
                            <div><Typography type={"headline"}>{this.props.chartName}</Typography></div>
                        </Grid>

                        {/* The chart */}
                        <Grid item style={{width: "100%"}}>
                            <div id="titanChart"></div>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
        )
    }
}