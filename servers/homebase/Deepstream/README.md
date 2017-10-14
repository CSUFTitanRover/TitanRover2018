# Deepstream Server

This deepstream server is tenative to change where it will be ran on: Homebase or Rover (Tegra)
For testing purposes we will be using the Deepstream Docker image to run the Deepstream server as a way to provide a consistent behavior in for
those of us programming in different enviroments e.g. Windows, Linux, Mac

_You need to have Docker installed in order to run the Deepstream docker container!_

## Installing Docker (Community Edition)

I would recommend downloading and installing docker-toolbox which is just a bundle installer that includes: Docker Engine, Compose, Machine, and Kitematic (GUI)
- Windows: https://www.docker.com/products/docker-toolbox
- Mac: https://www.docker.com/products/docker-toolbox

For linux everything is mainly done through the CLI
- Linux: 
  - Detailed Guide: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script
  - The 2 lines you need from the guide above: 
    - `curl -fsSL get.docker.com -o get-docker.sh`
    - `sudo sh get-docker.sh`

## Installing Deepstream through Docker

### Linux

Reference: https://deepstreamhub.com/open-source/install/docker-image/

1. Pull the docker image
    - `docker pull deepstreamio/deepstream.io`

2. Create a container to assign to deepstream
    - `docker create -t -p 6020:6020 -p 8080:8080 \
      --name deepstream.io \
      -v $(pwd)/conf:/usr/local/deepstream/conf \
      -v $(pwd)/var:/usr/local/deepstream/var \
      deepstreamio/deepstream.io`

3. Starting the deepstream docker container
    - `docker start -ia deepstream.io`

4. Stopping the deepstream docker container
    - `docker stop deepstream.io`

### Windows & Mac

If you installed docker through the docker-toolbox bundle then you should also have the GUI application called `Kitematic`.

1. In `Kitematic`, find the search bar and look for `deepstream.io`
2. Click the `Create` button
    - The deepstream container should automatically start. If not then find and click the start button in the Deepstream container.

Starting and stopping the deepstream container is as easy as just clicking the start and stop buttons :) 

## Deepstream Docker Container

The image exposes the following ports:

- 6020 - Websocket port
- 8080 - HTTP port


