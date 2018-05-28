import React, { Component } from 'react';
import PropTypes from 'prop-types';
import isEmpty from 'lodash.isempty';
import shortid from 'shortid';
import cn from 'classnames';
import remove from 'lodash.remove';
import Typography from '@material-ui/core/Typography';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import grey from '@material-ui/core/colors/grey';
import blueGrey from '@material-ui/core/colors/blueGrey';
import lightGreen from '@material-ui/core/colors/lightGreen';
import blue from '@material-ui/core/colors/blue';
import { withStyles } from '@material-ui/core/styles';
import DeepstreamPubSubProvider from '../../utils/DeepstreamPubSubProvider';
import { getClient } from '../../utils/deepstream';

const styles = theme => ({
  title: {
    padding: theme.spacing.unit * 2,
    background: theme.palette.primary.main,
    color: grey[50],
  },
  droppable: {
    padding: theme.spacing.unit * 2,
    background: blueGrey[50],
  },
  droppableIsDraggingOver: {
    background: blue[100],
  },
  draggable: {
    userSelect: 'none',
    padding: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit,
    background: grey[50],
  },
  draggableIsDragging: {
    background: lightGreen[100],
  },
  scrollContainer: {
    overflowX: 'hidden',
    overflowY: 'auto',
    maxHeight: '70vh', // will need to be customized for 1080p
  },
  deleteIcon: {
    marginLeft: theme.spacing.unit,
  },
});

// a little function to help us with reordering the result
const reorder = (list, startIndex, endIndex) => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};

class TemporaryWaypointsList extends Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
  }

  state = { data: [] }

  async componentDidMount() {
    this.client = await getClient();
    this.client.record.snapshot('temp/waypoints', (error, data) => {
      if (data && data.length > 0) {
        this.setState({ data });
      }
    });
  }

  handleNewPayload = (datum) => {
    const { data } = this.state;

    const transformedDatum = {
      id: shortid.generate(),
      content: datum,
    };

    const newData = [...data, transformedDatum];

    this.client.record.setData('temp/waypoints', newData);
    this.setState({ data: newData });
  }

  onDragEnd = (result) => {
    // dropped outside the list
    if (!result.destination) {
      return;
    }

    if (result.destination.index === result.source.index) {
      return;
    }

    const data = reorder(
      this.state.data,
      result.source.index,
      result.destination.index,
    );

    this.setState({ data });
    this.client.record.setData('temp/waypoints', data);
  };

  handleWaypointDelete = id => () => {
    const { data } = this.state;

    remove(data, x => x.id === id);

    this.client.record.setData('temp/waypoints', data);
    this.setState({ data });
  }

  renderDraggableItem = (item, index) => {
    const [latitude, longitude] = item.content;
    const { classes } = this.props;

    return (
      <Draggable key={item.id} draggableId={item.id} index={index}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            style={provided.draggableProps.style}
          >
            <ListItem className={cn(
              classes.draggable,
              { [classes.draggableIsDragging]: snapshot.isDragging },
            )}
            >
              <ListItemText>{`${index + 1}. `}<strong>Latitude: </strong>{`${latitude}, `}<strong>Longitude: </strong>{longitude}</ListItemText>
              <Button
                className={classes.button}
                variant="raised"
                color="secondary"
                onClick={this.handleWaypointDelete(item.id)}
              >
                Delete
                <DeleteIcon className={classes.deleteIcon} />
              </Button>
            </ListItem>
          </div>
        )}
      </Draggable>
    );
  }

  renderList = () => {
    const { data } = this.state;

    if (isEmpty(data)) {
      return <Typography variant="body1" color="textSecondary" align="center">No Staged Waypoints Found</Typography>;
    }

    return data.map((item, index) => this.renderDraggableItem(item, index));
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <DeepstreamPubSubProvider eventName="temp/waypoints:add" onNewPayload={this.handleNewPayload}>
          {() => (
            <div>
              <Typography variant="title" className={classes.title}>Staged Waypoints</Typography>
              <div>
                <DragDropContext onDragEnd={this.onDragEnd}>
                  <Droppable droppableId="droppable">
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        className={cn(
                          classes.droppable,
                          { [classes.droppableIsDraggingOver]: snapshot.isDraggingOver },
                        )}
                      >
                        <div className={classes.scrollContainer}>
                          {this.renderList()}
                        </div>
                        {provided.placeholder}
                      </div>
                    )}
                  </Droppable>
                </DragDropContext>
              </div>
            </div>
          )}
        </DeepstreamPubSubProvider >

      </div>
    );
  }
}

export default withStyles(styles)(TemporaryWaypointsList);
