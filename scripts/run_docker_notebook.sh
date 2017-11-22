#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

docker pull signetsim/notebook:develop
docker run -p 8888:8888 -d signetsim/notebook:develop