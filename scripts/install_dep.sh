apt-get update -qq

if [[ $(apt-cache search libsundials-serial | wc -l) -gt 0 ]]; then
    SUNDIALS_BIN="libsundials-serial"

elif [[ $(apt-cache search libsundials-nvecserial2 | wc -l) -gt 0 ]] && [[ $(apt-cache search libsundials-cvode2 | wc -l) -gt 0 ]] && [[ $(apt-cache search libsundials-ida2 | wc -l) -gt 0 ]] ; then
    SUNDIALS_BIN="libsundials-nvecserial2 libsundials-cvode2 libsundials-ida2"

else
    SUNDIALS_BIN=""

fi

if [[ $(apt-cache search libsundials-serial-dev | wc -l) -gt 0 ]]; then
    SUNDIALS_DEV="libsundials-serial-dev"

elif [[ $(apt-cache search libsundials-dev | wc -l) -gt 0 ]]; then
    SUNDIALS_DEV="libsundials-dev"

else
    SUNDIALS_DEV=""

fi

if [[ $(apt-cache search libatlas-dev | wc -l) -gt 0 ]]; then
    ATLAS_DEV="libatlas-dev"

elif [[ $(apt-cache search libatlas-base-dev | wc -l) -gt 0 ]]; then
    ATLAS_DEV="libatlas-base-dev"

else
    ATLAS_DEV=""

fi


apt-get install -y libopenmpi-dev openmpi-bin \
                    ${SUNDIALS_BIN} ${SUNDIALS_DEV} \
                    liblapack-dev libblas-dev ${ATLAS_DEV} \
                    python-pip python-dev make swig git

pip install -i https://pypi.python.org/simple pip --upgrade  --ignore-installed

if [ -f /usr/bin/pip ]
then
    mv /usr/bin/pip /usr/bin/pip.bak
fi
ln -s /usr/local/bin/pip /usr/bin/pip

if [ -f /usr/bin/pip2 ]
then
    mv /usr/bin/pip2 /usr/bin/pip2.bak
fi
ln -s /usr/local/bin/pip2 /usr/bin/pip2

pip2 install distribute setuptools --upgrade --ignore-installed
easy_install --upgrade distribute

# Version incompatibility issue... Hopefully temporary
pip2 install pyopenssl

# Checking if mpicc is in /usr/bin
if [ ! -f /usr/bin/mpicc ] ; then
    mpicc_path=$(echo $(find /usr -name mpicc) | cut -d' ' -f1)
    ln -s ${mpicc_path} /usr/bin
fi

# Checking if mpirun is in /usr/bin
if [ ! -f /usr/bin/mpirun ] ; then
    mpirun_path=$(echo $(find /usr -name mpirun) | cut -d' ' -f1)
    ln -s ${mpirun_path} /usr/bin

fi


# Checking if libatlas is in /usr/lib
if [ ! -f /usr/lib/libatlas.so ] ; then
    ATLAS_PATH=$(find /usr -name libatlas.so)
    if [ -z "${ATLAS_PATH}" ] ; then
        ATLAS_PATH=$(find /usr -name libtatlas.so)
    fi

    ln -s ${ATLAS_PATH} /usr/lib/libatlas.so
fi
