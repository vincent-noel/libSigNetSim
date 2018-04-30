apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    make swig python3-pip python3-dev

pip3 install pip --upgrade
if [ ! -f /usr/bin/pip3 ]
then
    ln -s /usr/local/bin/pip3 /usr/bin/pip3
fi

easy_install3 -U distribute
