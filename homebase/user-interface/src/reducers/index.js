import defaultStoreState from './defaultStoreState';

function appStore(state = defaultStoreState, action) {
  switch (action.type) {
    case 'OPEN_LEFT_MENU':
      return { ...state, leftMenuActive: true };
    case 'CLOSE_LEFT_MENU':
      return { ...state, leftMenuActive: false };
    case 'ADD_PLAYGROUND':
      return { ...state, playground: action.playground };
    default:
      return state;
  }
}

export default appStore;
