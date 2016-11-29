# libSigNetSim [![Build Status](https://travis-ci.org/vincent-noel/libSigNetSim.svg?branch=master)](https://travis-ci.org/vincent-noel/libSigNetSim)
Python library designed for building, adjusting and analyzing quantitative biological models.



##Non-Python Dependencies
You will need MPI libraries to execute C code in parallel

	libopenmpi-dev openmpi-bin


You will need Sundials library to perform numerical integration

	libsundials-serial-dev libsundials-serial


You will need Git to download the non-linear optimization library, and Pip to download python dependencies

	git python-pip



##Python dependencies

	pip install -r requirements.txt



##Installation
Still working on it. For now it should work just with

	python setup.py install



##License
	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	libSigNetSim is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	libSigNetSim is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with libSigNetSim. If not, see <http://www.gnu.org/licenses/>.
