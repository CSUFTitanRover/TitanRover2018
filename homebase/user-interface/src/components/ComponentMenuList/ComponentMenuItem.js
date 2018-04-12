import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import ChangeHistoryIcon from 'material-ui-icons/ChangeHistory';

/**
 * The ComponentMenuItem provides an easy way to define the text and icon of each menu item.
 */
class ComponentMenuItem extends Component {
  static propTypes = {
    /** The text for the menu item that will be displayed */
    title: PropTypes.string.isRequired,
    /** The text that will be displayed in the playground tab */
    componentname: PropTypes.string.isRequired,
    /** Provide your own Icon element to be shown instead of the default triangle icon */
    icon: PropTypes.element,
    className: PropTypes.string,
    componentprops: PropTypes.object,
  }

  static defaultProps = {
    icon: <ChangeHistoryIcon />,
    className: null,
    componentprops: null,
  }

  render() {
    const { title, icon, className, componentname, componentprops } = this.props;

    return (
      <ListItem
        button
        className={`playgroundDragSource ${className}`}
        data-title={title}
        data-componentname={componentname}
        data-componentprops={componentprops && JSON.stringify(componentprops)}
      >
        <ListItemIcon>
          {icon}
        </ListItemIcon>
        <ListItemText inset primary={title} />
      </ListItem>
    );
  }
}

export default ComponentMenuItem;
