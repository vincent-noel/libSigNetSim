apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    python-pip

pip install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute
