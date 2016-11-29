#!/bin/bash

cd docker
./build_image.sh ../
./run_container.sh
cd ..
