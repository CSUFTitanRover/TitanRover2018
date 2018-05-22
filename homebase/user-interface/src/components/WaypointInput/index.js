handleSubmit = (event) => {
  event.preventDefault();
  const lat = this.latitudeRef.value;
  const lon = this.longitudeRef.value;

  if (!lat || !lon) {
    toast.error('Latitude or Longitude cannot be empty!');
    return;
  }

  const waypoints = this.waypointsRecord.get();
  waypoints.push({ lat, lon });
  console.log(waypoints, typeof waypoints);
  this.waypointsRecord.set(waypoints);

  console.log(`Added the following to deepstream... Lat: ${lat}, Lon:${lon}`);

  this.latitudeRef.value = null;
  this.longitudeRef.value = null;
}


<form className={classes.container} noValidate autoComplete="off" onSubmit={this.handleSubmit}>
  <TextField
    inputRef={(ref) => { this.latitudeRef = ref; }}
    id="latitude"
    label="Latitude"
    className={classes.textField}
    margin="normal"
    type="number"
    step="any"
    required
  />
  <TextField
    inputRef={(ref) => { this.longitudeRef = ref; }}
    id="longitude"
    label="Longitude"
    className={classes.textField}
    margin="normal"
    type="number"
    step="any"
    required
  />
  <Button
    type="submit"
    variant="raised"
    color="primary"
    size="small"
    className={classes.button}
  >
    Add Coordinate
</Button>
