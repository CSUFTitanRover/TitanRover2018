export function addPlaygroundToStore(playground) {
  return {
    type: 'ADD_PLAYGROUND',
    playground,
  };
}

export default addPlaygroundToStore;
