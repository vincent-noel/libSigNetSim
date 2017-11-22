# libSigNetSim, Python library designed for building, adjusting and analyzing quantitative biological models.
[![Build Status](https://travis-ci.org/vincent-noel/libSigNetSim.svg?branch=master)](https://travis-ci.org/vincent-noel/libSigNetSim)
[![Coverage Status](https://coveralls.io/repos/github/vincent-noel/libSigNetSim/badge.svg?branch=master)](https://coveralls.io/github/vincent-noel/libSigNetSim?branch=master)
[![Documentation Status](https://readthedocs.org/projects/libsignetsim/badge/?version=master)](http://libsignetsim.readthedocs.io/en/master/)



## Non-Python Dependencies

    bash scripts/install_dep.sh



## Python dependencies

	pip install -r requirements.txt



## Installation

	python setup.py install



## Jupyter notebook with libSigNetSim

You can run a Jupyter notebook, in a virtual environment, using

	scripts/run_notebook.sh

You can also run a notebook in a docker, using

	docker pull signetsim/notebook
	docker run --name notebook -p 8888:8888 -d signetsim/notebook 

Both will start the notebook on localhost:8888
For the docker, password is the name of this repository
Some examples, using combine archives, are available in the notebooks folder

## License
	Copyright (C) 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)

	SigNetSim is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	SigNetSim is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with SigNetSim. If not, see <http://www.gnu.org/licenses/>.

## Financial support

	This program was developed within the CeTICS project, at the Butantan Institute.

<p align="center">
	<a href="http://cetics.butantan.gov.br"><img src="docs/logos/cetics.png" align="middle" hspace="50"></a>
	<a href="http://www.butantan.gov.br"><img src="docs/logos/butantan.png" width="300" align="middle" hspace="50"></a>
</p>

	The work was supported by grants #12/20186-9, #13/07467-1, and #13/24212-7
	of the São Paulo Research Foundation (FAPESP) and fellowships from CNPq.


<p align="center">
	<a href="http://www.fapesp.br"><img src="docs/logos/FAPESP.jpg" width="300" align="middle" hspace="50"></a>
	<a href="http://cnpq.br"><img src="docs/logos/CNPq.jpg" width="175" align="middle" hspace="50"></a>
</p>