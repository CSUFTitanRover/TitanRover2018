import appStore from './index';

describe('testing reducer logic', () => {
  test('testing opening left menu', () => {
    const state = {};
    const action = { type: 'OPEN_LEFT_MENU' };
    const result = appStore(state, action);
    const expectedResult = {
      leftMenuActive: true,
    };

    expect(result).toEqual(expectedResult);
  });

  test('testing closing left menu', () => {
    const state = {};
    const action = { type: 'CLOSE_LEFT_MENU' };
    const result = appStore(state, action);
    const expectedResult = {
      leftMenuActive: false,
    };

    expect(result).toEqual(expectedResult);
  });

  test('testing adding playground', () => {
    const state = {};
    const action = { type: 'ADD_PLAYGROUND', playground: '<Playground>' };
    const result = appStore(state, action);
    const expectedResult = {
      playground: '<Playground>',
    };

    expect(result).toEqual(expectedResult);
  });

  test('testing default case', () => {
    const state = {};
    const action = {};
    const result = appStore(state, action);
    const expectedResult = {};

    expect(result).toEqual(expectedResult);
  });
});
