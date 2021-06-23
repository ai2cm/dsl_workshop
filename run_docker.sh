#!/bin/bash
./setup/docker_setup
docker run --rm -p 8888:8888 -v $(pwd):/workshop workshop-jupyter
