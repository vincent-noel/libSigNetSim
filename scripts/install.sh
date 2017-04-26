#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

python $INSTALL_DIR/setup.py install
python $INSTALL_DIR/fix_libsedml_addChild.py;