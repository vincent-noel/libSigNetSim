#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

pip3 install -r $INSTALL_DIR/requirements.txt

pip3 install $INSTALL_DIR