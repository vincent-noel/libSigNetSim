apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    python-pip python-dev make swig git

pip install pip --upgrade --ignore-installed
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

# Version incompatibility issue... Hopefully temporary
pip2 install pyopenssl

