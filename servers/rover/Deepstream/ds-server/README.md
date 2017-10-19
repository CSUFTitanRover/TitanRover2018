# Rover Deepstream Server

This is the main directory for the official Deepstream server that will run on the Nvidia Tegra TX2.

Ports the DS rover server will listen on:

| Endpoint  | Address | PORT |
| --------- | ------- | ---- |
| Websocket | 0.0.0.0 | 4020 |
| HTTP      | 0.0.0.0 | 4080 |


## Starting the Rover Deepstream server

First install dependencies: `npm install`

Start the server: `npm start`