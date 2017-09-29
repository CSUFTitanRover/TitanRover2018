# User Interface | 2018

The User Interface will be written primarily using React for the frontend and Deepstream in the backend to handle all the real-time data updates. This will be a web application that is driven via real-time data and user interaction.

## Getting Started

If you don't have Node installed then follow this guide: [Installing Node.js](Installing-Node.md)

_You need to have Node installed in order to develop the UI_

### nvm (_skippable if you don't have nvm installed_)

If you have `nvm` installed, nvaigate to and open the **user-interface** folder and run the command: `nvm use`

This automatically sets your current node version to the version specified in the `.nvmrc` file found in the root of the project folder. It should set the current node version to `8.5.0`.

### npm (Node Package Manager)

`npm` is a package manager that is installed alongside Node itself. It allows you to install packages as well as manage your packages with ease. 

**Every time when freshly cloning this repo you must install dependencies first!**

In your command line:

1. Install dependencies
- longhand: `npm install`
- shorthand: `npm i`

2. Starting the dev server:
- longhand: `npm run start`
- shorthand: `npm start`

## Running unit tests

It's always important to write unit tests to double check that the any code we write will work. We use [Jest](https://facebook.github.io/jest/) to run our unit tests.

Run test watcher: 
- longhand: `npm run test`
- shorthand: `npm test`

## Building for production:

Running the build command will bundle, transpile, and minify our code as well as generating a **build** folder with all the code bundled up. We would really only use this command at the end when our UI is pretty much finished and ready.

Building our production ready UI: `npm run build`

----

This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).