if [ -z "$1" ]; then
    PYTHON_VERSION=3
else
    PYTHON_VERSION=$1
fi

if [[ "${PYTHON_VERSION}" == 2 ]]; then
    PYTHON_PACKAGES="python2-pip python2-devel"
    PIP_EXECUTABLE="pip2"

else
    PYTHON_PACKAGES="python3-pip python3-devel"
    PIP_EXECUTABLE="pip3"
fi

dnf -y update
dnf -y install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel atlas-static \
                ${PYTHON_PACKAGES} redhat-rpm-config \
                make

${PIP_EXECUTABLE} install -i https://pypi.python.org/simple pip --upgrade  --ignore-installed
${PIP_EXECUTABLE} install setuptools --upgrade --ignore-installed
if [[ "${PYTHON_VERSION}" == 3 ]]; then
    EASY_INSTALL=$(find /usr -name easy_install-3*)

    if [[ -z "${EASY_INSTALL}" ]]; then
        EASY_INSTALL="easy_install"
    fi

elif [[ "${PYTHON_VERSION}" == 2 ]]; then
    EASY_INSTALL=$(find /usr -name easy_install-2*)

    if [[ -z "${EASY_INSTALL}" ]]; then
        EASY_INSTALL="easy_install"
    fi

else
    EASY_INSTALL="easy_install"

fi
${EASY_INSTALL} --upgrade distribute

# Version incompatibility issue... Hopefully temporary
${PIP_EXECUTABLE} install pyopenssl

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