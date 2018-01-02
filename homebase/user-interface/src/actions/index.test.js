import { openLeftMenu, closeLeftMenu } from './menu';
import { addPlaygroundToStore } from './goldenLayout';

describe('testing actions', () => {
  test('testing openLeftMenu action', () => {
    const result = openLeftMenu();
    const expectedResult = {
      type: 'OPEN_LEFT_MENU',
    };

    expect(result).toEqual(expectedResult);
  });

  test('testing closeLeftMenu action', () => {
    const result = closeLeftMenu();
    const expectedResult = {
      type: 'CLOSE_LEFT_MENU',
    };

    expect(result).toEqual(expectedResult);
  });

  test('testing addPlaygroundToStore action', () => {
    const result = addPlaygroundToStore('<GL_LAYOUT>');
    const expectedResult = {
      type: 'ADD_PLAYGROUND',
      playground: '<PLAYGROUND>',
    };

    expect(result).toEqual(expectedResult);
  });
});
