import { openLeftMenu, closeLeftMenu } from './menu';

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
});
