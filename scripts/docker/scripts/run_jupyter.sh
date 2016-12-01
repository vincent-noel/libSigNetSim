#!/bin/bash
source /root/libSigNetSim/venv/bin/activate
jupyter notebook --ip 0.0.0.0 --no-browser
deactivate
