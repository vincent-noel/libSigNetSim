#!/bin/bash

cd /root/libSigNetSim
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
pip install jupyter
deactivate
cd ../..
