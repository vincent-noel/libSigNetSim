dnf -y update
dnf -y install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel atlas-static \
                python2-pip python2-devel redhat-rpm-config \
                make

pip install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute

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