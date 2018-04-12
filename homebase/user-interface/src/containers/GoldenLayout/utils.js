import Camera from '../../components/Camera/';
import DefaultChart from '../../components/DefaultChart/';
import RealtimeChart from '../../components/RealtimeChart/';
import RoverApiSettings from '../../components/RoverApiSettings/';
import StartAutonomyButton from '../../components/Autonomy/StartAutonomyButton';
import ResizeAwareMap from '../../components/ResizeAwareMap/';

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
  glNode.registerComponent('ResizeAwareMap', ResizeAwareMap);
  glNode.registerComponent('Camera', Camera);
  glNode.registerComponent('DefaultChart', DefaultChart);
  glNode.registerComponent('RoverApiSettings', RoverApiSettings);
  glNode.registerComponent('StartAutonomyButton', StartAutonomyButton);
  glNode.registerComponent('RealtimeChart', RealtimeChart);
}

export function initializeGL(glNode) {
  registerGLComponents(glNode);

  glNode.init();

  window.addEventListener('resize', () => {
    glNode.updateSize();
  });

  connectDragSources(glNode);
}
