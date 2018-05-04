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

easy_install3 -U distribute
