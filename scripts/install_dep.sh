apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    python-pip python-dev make swig

pip2 install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip2 /usr/bin/pip2
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute

pip install pyopenssl