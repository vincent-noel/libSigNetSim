dnf -y update
dnf -y install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel atlas-static \
                python2-pip python2-devel redhat-rpm-config \
                git gcc gcc-c++ make unzip wget curl

pip install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute

# Installing dependencies for python-libsedml
curl -sL https://raw.githubusercontent.com/vincent-noel/python-libsedml/master/scripts/install_dep_fedora.sh | bash -