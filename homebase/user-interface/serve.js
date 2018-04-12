const serve = require('serve');

serve(
  `${__dirname}/build`,
  {
    port: 3000,
    ignore: ['node_modules'],
    single: true,
  },
);

