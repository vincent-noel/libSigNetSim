apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    python-dev python-pip \
                    git g++ gcc make unzip wget \
                    subversion \
                    cmake swig \
                    zlib1g-dev libxml2-dev libbz2-dev \
                    libcurl4-openssl-dev \
                    libxslt1-dev

pip install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi
easy_install -U distribute

