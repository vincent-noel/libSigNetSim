#!/bin/bash
SRCDIR=$1

if [[ -n "$SRCDIR" ]]; then

	mkdir libSigNetSim
	cp ../$SRCDIR/requirements.txt libSigNetSim/
	cp ../$SRCDIR/setup.py libSigNetSim/
	cp -r ../$SRCDIR/libsignetsim libSigNetSim/

	docker build -t='notebook' .
	rm -fr libSigNetSim
fi

