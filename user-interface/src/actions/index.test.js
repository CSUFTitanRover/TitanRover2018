import { openLeftMenu, closeLeftMenu, addGoldenLayoutToStore } from './index';

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

  test('testing addGoldenLayoutToStore action', () => {
    const result = addGoldenLayoutToStore('<GL_LAYOUT>');
    const expectedResult = {
      type: 'ADD_GOLDEN_LAYOUT',
      glLayout: '<GL_LAYOUT>',
    };

    expect(result).toEqual(expectedResult);
  });
});
