React
=====

`React <https://reactjs.org/>`_ is a javascript library created by Facebook and provides a way
to create user interfaces in a declarative, efficient, and flexible way.

Learning React
--------------

Assuming that you have some programming experience and have a dirve for self-learning, here are some tutorials to
get you started:

#. `Facebook Official Tutorial <https://reactjs.org/tutorial/tutorial.html>`_
#. `React Video Series <https://www.youtube.com/watch?v=MhkGQAoc7bc&list=PLoYCgNOIyGABj2GQSlDRjgvXtqfDxKm5b>`_
#. `React-js-in-design-patterns <http://krasimirtsonev.com/blog/article/react-js-in-design-patterns>`_
#. `Creating a react application <https://egghead.io/lessons/react-bootstrap-a-react-application-through-the-cli-with-create-react-app>`_ (create a free account to access more videos in the series)

npm commands
------------

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
* ``npm run serve`` - serves the built user interface locally on port 3000
* ``npm run eject`` - ejects the project from the create-react-app configuration **DO NOT USE THIS UNLESS DIRECTED TO**

create-react-app
----------------

We used `create-react-app <https://github.com/facebookincubator/create-react-app>`_ to bootstrap the 
development process of our react application. create-react-app is a command-line (CLI) tool that generates
a project and hides away all the configuration process necessary for development. This means, we can focus
just on coding the react app instead of having to configure the project beforehand. You **do not** need to
install the create-react-app CLI tool as the user interface project folder has everything already set up.
