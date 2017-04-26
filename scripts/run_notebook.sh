#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

virtualenv venv
source venv/bin/activate
pip install -r $INSTALL_DIR/requirements.txt
pip install $INSTALL_DIR
pip install jupyter
jupyter notebook
deactivate
rm -r venv
