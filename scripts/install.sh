#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

pip2 install -r $INSTALL_DIR/requirements.txt

pip2 install $INSTALL_DIR
