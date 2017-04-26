#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

docker build -t libsignetsim-notebook $DIR/docker
docker run -d -p 8888:8888 signetsim/jupyter-notebook:xenial jupyter notebook --allow-root --no-browser --ip=0.0.0.0