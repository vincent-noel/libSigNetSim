#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

pip install -r $INSTALL_DIR/requirements.txt

pip install $INSTALL_DIR
