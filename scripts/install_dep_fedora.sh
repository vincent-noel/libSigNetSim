dnf -y update
dnf -y install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel atlas-static \
                python2-pip python2-devel redhat-rpm-config \

pip install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute
