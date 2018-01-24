import { addPlaygroundToStore } from './goldenLayout'

test('testing addPlaygroundToStore action', () => {
  const result = addPlaygroundToStore('<PLAYGROUND>');
  const expectedResult = {
    type: 'ADD_PLAYGROUND',
    playground: '<PLAYGROUND>',
  };

  expect(result).toEqual(expectedResult);
});