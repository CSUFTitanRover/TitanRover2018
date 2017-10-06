function appStore(state = {}, action) {
  switch (action.type) {
    case 'OPEN_LEFT_MENU':
      return { ...state, leftMenuActive: true };
    case 'CLOSE_LEFT_MENU':
      return { ...state, leftMenuActive: false };
    case 'ADD_GOLDEN_LAYOUT':
      return { ...state, glLayout: action.glLayout };
    default:
      return state;
  }
}

export default appStore;
