#!/bin/bash
./setup/docker_setup
docker run -p 8888:8888 -v $(pwd):/workshop workshop-jupyter
