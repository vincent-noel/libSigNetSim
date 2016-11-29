FROM ubuntu

MAINTAINER Vincent Noel version: 0.1

ADD scripts/install.sh /
RUN /bin/bash /install.sh

ADD libSigNetSim/ /root/libSigNetSim/
ADD scripts/install_signetsim.sh /
RUN /bin/bash /install_signetsim.sh

EXPOSE 8888
ADD scripts/run_jupyter.sh /
#RUN /bin/bash /run_jupyter.sh
