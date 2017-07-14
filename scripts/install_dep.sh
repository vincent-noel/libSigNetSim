apt-get update -qq
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
                    python-dev python-pip \
                    git g++ gcc make unzip wget curl



# Installing pip update if pip version < 9.0.1
currentver="$(pip --version | cut -d" " -f2)"
requiredver="9.0.1"
if [ "$(printf "$requiredver\n$currentver" | sort -V | head -n1)" == "$requiredver" ]; then
    pip install pip --upgrade
    if [ ! -f /usr/bin/pip ]
    then
        ln -s /usr/local/bin/pip /usr/bin/pip
    fi
fi


easy_install -U distribute

# Installing dependencies for python-libsedml
curl -sL https://raw.githubusercontent.com/vincent-noel/python-libsedml/develop/scripts/install_dep.sh | bash -