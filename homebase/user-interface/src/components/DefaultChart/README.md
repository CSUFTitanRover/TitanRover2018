Feel free to mess around with the example by adding in new data points or changing the chart type.

```js
const d = [
{
    "timestamp": 1519430037806,
    "ec": 7.7782,
    "humidity": 20
},
{
    "timestamp": 1519430038309,
    "ec": 11.8377,
    "humidity": 21
},
{
    "timestamp": 1519430038811,
    "ec": 8.4324,
    "humidity": 22
},
{
    "timestamp": 1519430039313,
    "ec": 8.8265,
    "humidity": 19
}];

<DefaultChart chartName="An optional Chart Name" data={d} chartType="line" />
```

