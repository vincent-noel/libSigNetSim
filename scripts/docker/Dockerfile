FROM signetsim/signetsim:xenial

MAINTAINER Vincent Noel version: 0.1

RUN git clone -b develop https://github.com/vincent-noel/libSigNetSim.git
RUN apt-get install -y libopenmpi-dev openmpi-bin libsundials-serial-dev libsundials-serial liblapack-dev libblas-dev libatlas-dev libfreetype6-dev libpng12-dev libatlas-base-dev python-dev python-pip python-setuptools git subversion gfortran g++ gcc make pkg-config unzip wget
RUN pip install -r /libSigNetSim/requirements.txt
RUN pip install /libSigNetSim
RUN pip install jupyter
RUN jupyter notebook --generate-config --allow-root
RUN printf "c = get_config()\nc.NotebookApp.password = u'sha1:1d43c5e9ef6c:74e8d4d9f0da82f442ee54ced5b11eb45a969bab'" >> /root/.jupyter/jupyter_notebook_config.py
EXPOSE 8888
