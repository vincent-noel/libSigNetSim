#!/bin/bash
apt-get update 
apt-get upgrade -y
apt-get install -y virtualenv git make \
	python-dev g++ \
	libopenmpi-dev openmpi-bin \
	apache2 libapache2-mod-wsgi \
	libsundials-serial-dev libsundials-serial
apt-get clean
