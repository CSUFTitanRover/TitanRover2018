React
=====

`React <https://reactjs.org/>`_ is a javascript library created by Facebook and provides a way
to create user interfaces in a declarative, efficient, and flexible way.

create-react-app
----------------

We used `create-react-app <https://github.com/facebookincubator/create-react-app>`_ to bootstrap the 
development process of our react application. create-react-app is a command-line (CLI) tool that hides 
away all the configuration process necessary for development. This means, we can focus just on coding 
the react app instead of having to configure the project beforehand. You **do not** need to install the
create-react-app CLI tool as the user interface project folder has everything already set up.


npm commands
^^^^^^^^^^^^

Here are a list of npm commands that have been set up for typical use when developing the UI:

* ``npm start`` - starts a dev server that serves the UI and auto reloads on changes
* ``npm test`` - runs the unit tests
* ``npm run styleguide`` - starts a `styleguidist <https://react-styleguidist.js.org/>`_ server 
* ``npm run lint`` - runs ESLint on the project to enfore the project defined coding standard
* ``npm run lint:fix`` - runs ESLint on the project and tries to auto-fix any errors found

The following npm commands aren't for typical use when developing the UI:

* ``npm run build`` - transpiles and minifies a production ready application
* ``npm run styleguide:build`` - builds a static styleguide website with our component documentation 
* ``npm run report-coverage`` - reports code coverage to `codecov <https://codecov.io>`_
* ``npm run eject`` - ejects the project from the create-react-app configuration **DO NOT USE THIS UNLESS DIRECTED TO**
