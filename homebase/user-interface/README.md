# User Interface | 2018

[![Node v8.5.0](https://img.shields.io/badge/node-v8.8.1-blue.svg
)]()
[![Build Status](https://travis-ci.org/CSUFTitanRover/TitanRover2018.svg?branch=feature%2FUserInterface)](https://travis-ci.org/CSUFTitanRover/TitanRover2018)
[![codecov](https://codecov.io/gh/CSUFTitanRover/TitanRover2018/branch/feature/UserInterface/graph/badge.svg)](https://codecov.io/gh/CSUFTitanRover/TitanRover2018/branch/feature%2FUserInterface)
[![User Interface](https://img.shields.io/badge/netlify-user_interface-39AFBC.svg)](https://userinterface2018.netlify.com/)
[![Styleguide](https://img.shields.io/badge/netlify-styleguide-39AFBC.svg)](https://userinterface2018-styleguide.netlify.com/)

The User Interface will be written primarily using React for the frontend and Deepstream in the backend to handle all the real-time data updates. This will be a web application that is driven via real-time data and user interaction.

## Getting Started

If you don't have Node installed then follow this guide: [Installing Node.js](Installing-Node.md)

_You need to have Node installed in order to develop the UI_

### nvm (_skippable if you don't have nvm installed_)

If you have `nvm` installed, navigate to and open the **user-interface** folder and run the command: `nvm use`

This automatically sets your current node version to the version specified in the `.nvmrc` file found in the root of the project folder. It should set the current node version to `8.8.1`.

### npm (Node Package Manager)

`npm` is a package manager that is installed alongside Node itself. It allows you to install packages as well as manage your packages with ease.

#### Install Dependencies

**Important: Every time when freshly cloning this repo or pulling new changes with new package dependencies you must install dependencies first!**

In your command line, install dependencies:
- longhand: `npm install`
- shorthand: `npm i`

#### Installing packages

Installing packages can be done through npm. When installing packages with **npm version 5.x & up**, it will automatically save your package's info to `package.json`. If you feel the need to specify npm to save the package info then you can add the flag `-P` (shorthand) or `--save-prod` (longhand).

If you have a version of npm below `v5.0` then you can add the `--save` flag to save your package's info to `package.json`

Installing packages through npm v5.x can be done so by:
- longhand: `npm install <package_name>`
- shorthand: `npm i <package_name>`
- _(Optional)_ With save flag: `npm i -P <package_name>`

Installing via npm v4.x and below
- longhand: `npm install --save <package_name>`
- shorthand: `npm i -s <package_name>`

#### Running the UI Dev Server

The UI dev server runs on `port 3000` by default.

1. In your command line, start the UI dev server:
- longhand: `npm run start`
- shorthand: `npm start`

2. If there were no issues, open `localhost:3000` in your browser.

#### Running unit tests

It's always important to write unit tests to double check that any code we write will work. We use [Jest](https://facebook.github.io/jest/) to run our unit tests.

When writing Components or any JS files you should format your test file names like so: `<file_name>.test.js`.

Any javascript code you write should have a `*.test.js` sibling file.
This couples your code and test files together in the same directory.

E.g.

```
components/
    MyComponent/
        - index.js
        - index.test.js
        - README.md
```

Run test watcher and execute tests:
- longhand: `npm run test`
- shorthand: `npm test`

You can look at this guide for more information: [Running Tests](https://github.com/facebookincubator/create-react-app/blob/master/packages/react-scripts/template/README.md#running-tests)

#### Building for production:

Running the build command will bundle, transpile, and minify our code as well as generate a **build** folder with all the code bundled up. We would really only use this command at the end when our UI is pretty much finished and ready.

Building our production ready UI: `npm run build`

## Using Styleguidist

[Styleguidist](https://github.com/styleguidist/react-styleguidist) is used to develop components in a standalone enviroment separate from the UI itself. It also serves as a way to generate documentation for the components that we have built by hand.

You can take a look at our styleguide here: [current styleguide](./src/styleguide/index.html)

**Important: It's required to develop your components using Styleguidist.**

### Requirements for Styleguidist:

`Styleguidist` expects your components to be inside either the `components/` or `containers/` folder and will search for files ending in `.js`.

1. Create a folder with the name of your component
    - e.g. components/MyComponent/
2. Create an `index.js` file
    - e.g. components/MyComponent/index.js
3. Create a `README.md` file inside your `Component` folder
    - e.g. components/MyComponent/README.md
4. Document your `README.md` file
    - [Usage Examples and README Files](https://react-styleguidist.js.org/docs/documenting.html#usage-examples-and-readme-files)

### Running the Styleguide dev server

The styleguide dev server runs on `port 6060` by default.
1. Run styleguid dev server: `npm run styleguide`
2. Open `localhost:6060` in your browser.

### Building the Styleguide

This is similar as to running `npm run build` however it generates and bundles the styleguide. When building the styleguide or running the styleguide dev server, styleguidist will look for both `index.js` and `README.md` files to parse and generate the necessary docs.

Building the styleguide: `npm run styleguide:build`

## Standard Coding Style

In order to make sure everyone is coding in the same style we will be using ESLint to enforce a standard style.

We will be using the standard the company Airbnb uses.

- Style guide for Javascript: https://github.com/airbnb/javascript
- Style guide for React: https://github.com/airbnb/javascript/tree/master/react

I tweaked the rules to allow `JSX` inside `*.js` files but other than that simple change the Airbnb styles hold true.

## ESLint

In order to take advantage of ESLint there are npm command scripts defined for you. If you get any errors like below when running any of the npm commands do not be afraid! ESLint will return a non-zero exit status which defines that there are lint errors. If you run the linting commands and you get no exit errors then your code passes ESLint! (ESLint prefers to be silent on success)

```js
// Example error output if ESLint has linting error
npm ERR! code ELIFECYCLE
npm ERR! errno 1
npm ERR! user-interface@0.1.0 lint: `eslint .`
npm ERR! Exit status 1
npm ERR!
npm ERR! Failed at the user-interface@0.1.0 lint script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output above.

npm ERR! A complete log of this run can be found in:
npm ERR!     /home/weffe/.npm/_logs/2017-09-30T02_20_11_174Z-debug.log
```

### lint

This npm command will lint the entire UI project for any errors. It will output any errors it finds into the console.

Command: `npm run lint`

### lint:fix

This npm command will make ESLint fix any errors it can while linting the entire UI project. There's a possibility that ESLint won't be able to fix all the errors and that will be left to you to do by hand.

Command: `npm run lint:fix`

### ESLint with VSCode

I have included specific config files for VSCode to take advantage of ESLint. In order for this to work, you will also need to install the [ESLint extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) from the Marketplace. Using eslint through VSCode allows you to skip having to run the npm commands.

Features:
- Auto Lints & fixes errors on file save.
- Shows linting errors in the editor itself along with the terminal.

## Text Editors or IDEs

I personally use [VSCode](https://code.visualstudio.com/) (free download) to develop the UI in.

You can also take a look at:
- [Atom](https://atom.io/) (free download)
- [Webstorm](https://www.jetbrains.com/webstorm/) (free download with student email)


## VSCode

I have included a `extensions.json` file in the `.vscode` folder that will be parsed by VSCode when opening the project. It will auto-suggest you install the recommended extensions if you do not already have them installed. I highly encourage you do!

There is also a `settings.json` file that is configured to allow the ESLint extension to do it's thing.

## Typical Workflow

A typical workflow for developing the User Interface will look like this.

1. `git pull` for new updates if there are any.
2. Install any new dependencies: `npm i`
3. _(Optional)_ Install new packages: `npm i <package_name>`
4. Start the `styleguide` dev server: `npm run styleguide`
5. Do your development work.
6. Lint & fix your code: `npm run lint:fix`

## Travis CI

We use [Travis CI](https://travis-ci.org/) to continuously test our UI when a commit is pushed to the repo or a pull-request is made.
This allows us to be able to sleep well at night that if something breaks we will hear about it.
[Check out our travis build](https://travis-ci.org/CSUFTitanRover/TitanRover2018).

## CodeCov

We use [CodeCov](https://codecov.io/) to monitor our code coverage for the UI. This means knowing at all times how much unit testing we have across our UI project.
[Check us out on CodeCov](https://codecov.io/gh/CSUFTitanRover/TitanRover2018/branch/feature%2FUserInterface).

## Netlify

We use [Netlify](https://www.netlify.com/) to build and update our User Interface and Styleguide webpage on every push and pull-request. This means whenever accessing
the webpages they are the latest version. This way you can stay up to date with the progress of how both pages are looking.

Check out our User Interface: https://userinterface2018.netlify.com/

Check out our Styleguide: https://userinterface2018-styleguide.netlify.com/

## Configuration Files

You may be wondering what all the `.<config>` files are for so I thought it would be nice to list them here.

- `.editorconfig` - EditorConfig helps developers define and maintain consistent coding styles between different editors and IDEs. [Learn More](http://editorconfig.org/)
- `.eslintrc.json` - Configuration file for ESLint that specifies rules, parser options, enviroments, etc. [Learn More](https://eslint.org/docs/user-guide/configuring)
- `.eslintignore` - This file is like `.gitignore` and specifies a list of files or directories for ESLint to ignore when linting the UI project.
- `styleguide.config.js` - This is a config file for Styleguidist. Currenty it just specifies how Styleguidist should search for components. [Learn More](https://react-styleguidist.js.org/docs/configuration.html)


## Learn more about ES6 Javascript

If you are interested in learning more about ES6 javascript then check these guides out:

- http://stack.formidable.com/es6-interactive-guide/#/
- https://babeljs.io/learn-es2015/

----

This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).
