#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`




cd /root

svn checkout http://svn.code.sf.net/p/sbml/code/trunk/libsbml/ libsbml
cd libsbml

mkdir build
cd build

cmake -DENABLE_COMP=ON -DENABLE_FBC=ON -DENABLE_LAYOUT=ON -DENABLE_QUAL=ON -DENABLE_GROUPS=ON -DENABLE_MULTI=ON -DWITH_EXAMPLES=ON -DWITH_PYTHON=ON -DLIBSBML_USE_LEGACY_MATH=ON ..
make
make install

cd ../..

git clone https://github.com/NuML/NuML.git
cd NuML/libnuml

mkdir build
cd build

cmake -DEXTRA_LIBS="xml2;z;bz2;" -DLIBSBML_STATIC=ON -DWITH_EXAMPLES=ON -DWITH_PYTHON=ON ..
make
make install

cd ../../..

git clone https://github.com/vincent-noel/libSEDML.git
cd libSEDML

mkdir build
cd build

cmake -DEXTRA_LIBS="xml2;z;bz2;" -DLIBSBML_STATIC=ON -DLIBNUML_STATIC=ON -DWITH_EXAMPLES=ON -DWITH_PYTHON=ON ..
make
make install

cd ../..

ln -s /usr/local/lib/python2.7/site-packages/{libsbml*,libsedml*,libnuml*} /usr/local/lib/python2.7/dist-packages/

cd ${EXEC_DIR}

pip install -r $INSTALL_DIR/requirements.txt

python $INSTALL_DIR/setup.py install
#python $INSTALL_DIR/fix_libsedml_addChild.py;