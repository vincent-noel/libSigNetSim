#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

if [[ -n "$1" ]] && [[ "$1" == 2 ]] ; then
    PIP_EXECUTABLE="pip2"
else
    PIP_EXECUTABLE="pip3"
fi

${PIP_EXECUTABLE} install -r $INSTALL_DIR/requirements.txt

${PIP_EXECUTABLE} install $INSTALL_DIR
