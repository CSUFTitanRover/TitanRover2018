import Counter from '../../components/Counter';

/**
 * Registers all react components to the passed in GL node.
 * @param {GoldenLayout} glNode
 */
export function registerGLComponents(glNode) {
  glNode.registerComponent('Counter', Counter);
}

export function initializeGL(glNode) {
  registerGLComponents(glNode);

  glNode.init();

  window.addEventListener('resize', () => {
    glNode.updateSize();
  });

  connectDragSources(glNode)
}

/**
 * 
 * @param {string} title - The title that will be displayed in the tab when the component mounts in the Playground 
 * @param {string} componentName - The case-sensitive component name that must match an exisiting registered GL component
 * @param {HTMLElement} element - The source html dom element the drag source function will bind to
 * @param {GoldenLayout} glNode
 */
export function connectDragSource(title, componentname, element, glNode) {
  const newDragSourceConfig = {
    title: title,
    type: 'react-component',
    component: componentname,
  };

  glNode.createDragSource(element, newDragSourceConfig);
}

export function connectDragSources(glNode) {
  const dragSourceElements = document.querySelectorAll('.playgroundDragSource');

  dragSourceElements.forEach(element => {
    const { title, componentname } = element.dataset;
    connectDragSource(title, componentname, element, glNode);
  })
}

