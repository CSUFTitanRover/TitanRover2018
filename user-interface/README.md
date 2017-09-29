# User Interface | 2018

The User Interface will be written primarily using React for the frontend and Deepstream in the backend to handle all the real-time data updates. This will be a web application that is driven via real-time data and user interaction.

----

## Getting Started

If you don't have Node installed then follow this guide: [Installing Node.js](Installing-Node.md)

_You need to have Node installed in order to develop the UI_

### nvm (_skippable if you don't have nvm installed_)

If you have `nvm` installed, nvaigate to and open the **user-interface** folder and run the command: `nvm use`

This automatically sets your current node version to the version specified in the `.nvmrc` file found in the root of the project folder. It should set the current node version to `8.5.0`.

### npm (Node Package Manager)

`npm` is a package manager that is installed alongside Node itself. It allows you to install packages as well as manage your packages with ease. 

#### Install Dependencies

**Every time when freshly cloning this repo you must install dependencies first!**

In your command line, install dependencies:
- longhand: `npm install`
- shorthand: `npm i`

#### Installing packages

Installing packages can be done through npm. When installing packages with `npm version 5.x & up`, it will automatically save your package's info to `package.json`. If you feel the need to specify npm to save the package info then you can add the flag `-P` (shorthand) or `--save-prod` (longhand).

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

Run test watcher: 
- longhand: `npm run test`
- shorthand: `npm test`

You can look at this guide for more information: [Running Tests](https://github.com/facebookincubator/create-react-app/blob/master/packages/react-scripts/template/README.md#running-tests)

#### Building for production:

Running the build command will bundle, transpile, and minify our code as well as generate a **build** folder with all the code bundled up. We would really only use this command at the end when our UI is pretty much finished and ready.

Building our production ready UI: `npm run build`

----

## Using Styleguidist

[Styleguidist](https://github.com/styleguidist/react-styleguidist) is used to develop components in a standalone enviroment separate from the UI itself. It also serves as a way to generate documentation for the components that we have built by hand. 

**\* It's required to develop your components using Styleguidist.**

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

----

## Coding Style Guide

`TODO`

## Typical Workflow

A typical workflow for developing the User Interface will look like this.

1. `git pull` for new updates if there are any.
2. Install any new dependencies: `npm i`
3. _(Optional)_ Install new packages: `npm i <package_name>`
3. Start the `styleguide` dev server: `npm run styleguide`
4. Do your development work.

----

## Text Editors or IDEs

I personally use [VSCode](https://code.visualstudio.com/) (free download) to develop the UI in.

You can also take a look at:
- [Atom](https://atom.io/) (free download)
- [Webstorm](https://www.jetbrains.com/webstorm/) (free download with student email)

----

This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).