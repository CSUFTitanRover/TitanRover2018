import Counter from '../../components/Counter';
import Camera from '../../components/Camera/';
import Chart from '../../components/Chart/';
import RoverApiSettings from '../../components/RoverApiSettings/';


/**
 * @param {string} title - The title that will be displayed in the Playground tab
 * @param {string} componentname - The component name must match a registered GL component
 * @param {HTMLElement} element - The source html dom element the drag source function will bind to
 * @param {GoldenLayout} glNode
 */
export function connectDragSource(title, componentname, componentprops = null, element, glNode) {
  const newDragSourceConfig = {
    title,
    type: 'react-component',
    component: componentname,
  };

  if (componentprops) {
    newDragSourceConfig.props = JSON.parse(componentprops);
  }

  glNode.createDragSource(element, newDragSourceConfig);
}

export function connectDragSources(glNode) {
  const dragSourceElements = document.querySelectorAll('.playgroundDragSource');

  dragSourceElements.forEach((element) => {
    const { title, componentname, componentprops } = element.dataset;
    connectDragSource(title, componentname, componentprops, element, glNode);
  });
}

/**
 * Registers all react components to the passed in GL node.
 * @param {GoldenLayout} glNode
 */
export function registerGLComponents(glNode) {
  glNode.registerComponent('Counter', Counter);
  glNode.registerComponent('Camera', Camera);
  glNode.registerComponent('Chart', Chart);
  glNode.registerComponent('RoverApiSettings', RoverApiSettings);
}

export function initializeGL(glNode) {
  registerGLComponents(glNode);

  glNode.init();

  window.addEventListener('resize', () => {
    glNode.updateSize();
  });

  connectDragSources(glNode);
}
