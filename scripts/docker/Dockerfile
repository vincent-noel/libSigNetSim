FROM debian:stretch

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update

ADD . /libSigNetSim

RUN /bin/bash /libSigNetSim/scripts/install_dep.sh 2
RUN pip install -r /libSigNetSim/requirements.txt
RUN pip install /libSigNetSim
RUN pip install "jupyter<= 6"
RUN jupyter notebook --generate-config --allow-root
RUN printf "c = get_config()\nc.NotebookApp.password = u'sha1:1d43c5e9ef6c:74e8d4d9f0da82f442ee54ced5b11eb45a969bab'" >> /root/.jupyter/jupyter_notebook_config.py

EXPOSE 8888

CMD cd libSigNetSim/notebooks; jupyter notebook --allow-root --no-browser --ip=0.0.0.0
