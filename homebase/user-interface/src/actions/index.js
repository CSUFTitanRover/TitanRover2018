export function openLeftMenu() {
  return {
    type: 'OPEN_LEFT_MENU',
  };
}

export function closeLeftMenu() {
  return {
    type: 'CLOSE_LEFT_MENU',
  };
}

export function addGoldenLayoutToStore(glLayout) {
  return {
    type: 'ADD_GOLDEN_LAYOUT',
    glLayout,
  };
}
