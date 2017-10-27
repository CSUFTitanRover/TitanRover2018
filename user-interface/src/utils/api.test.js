import { add5 } from './api';

test('add5 with 3 to be 8', () => {
  const initValue = 3;
  const result = add5(initValue);

  expect(result).toBe(8);
});
