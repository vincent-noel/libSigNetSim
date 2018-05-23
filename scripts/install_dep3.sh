apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    make swig python3-pip python3-dev git

pip3 install pip --upgrade --ignore-installed
if [ -f /usr/bin/pip ]
then
    mv /usr/bin/pip /usr/bin/pip.bak
fi
ln -s /usr/local/bin/pip /usr/bin/pip

if [ -f /usr/bin/pip3 ]
then
    mv /usr/bin/pip3 /usr/bin/pip3.bak
fi
ln -s /usr/local/bin/pip3 /usr/bin/pip3

pip3 install distribute setuptools --upgrade --ignore-installed

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
