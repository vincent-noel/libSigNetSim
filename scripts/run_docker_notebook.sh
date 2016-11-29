#!/bin/bash
DIR=`dirname $0`
cd $DIR/docker
./build_image.sh ../
./run_container.sh
cd ..
