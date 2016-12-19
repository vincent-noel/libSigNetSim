#!/bin/bash
source /root/libSigNetSim/venv/bin/activate
python -m unittest discover libsignetsim/ -v
deactivate
