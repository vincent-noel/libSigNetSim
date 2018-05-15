#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This file is part of libSigNetSim.
#
# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libSigNetSim.  If not, see <http://www.gnu.org/licenses/>.

"""

	Initialization of the module SigNetSim

"""
from __future__ import absolute_import, unicode_literals, print_function

import matplotlib
matplotlib.use("agg", warn=False)

from .combine import (
	CombineArchive, CombineException, FileNotFoundException, NotAZipFileException, NoManifestFoundException,
	NoMasterSedmlFoundException, NoMasterSbmlFoundException, NoMasterNumlFoundException, NoSedmlFoundException
)
from .settings import Settings
from .continuation import EquilibriumPointCurve
from .data import Experiment
from .numl import NuMLDocument, NuMLException, NuMLFileNotFound
from .sedml import (
	SedmlDocument, SedmlException, SedmlMathException, SedmlFileNotFound, SedmlMixedSubtasks,
	SedmlModelLanguageNotSupported, SedmlModelNotFound, SedmlModelObjectNotFound, SedmlMultipleModels,
	SedmlNotImplemented, SedmlOneStepTaskException, SedmlUnknownURI, SedmlUnknownXPATH
)
from .simulation import (
	TimeseriesSimulation, SteadyStatesSimulation, SimulationCompilationException, SimulationExecutionException,
	SimulationNoDataException, SimulationException
)

from .optimization import ModelVsTimeseriesOptimization, OptimizationException

from .model import (
	Model, SbmlDocument, MathFormula, KineticLaw,
	ModelException, SbmlException, FileException,
	MissingModelException, MissingSubmodelException,
	PackageNotImplementedModelException, TagNotImplementedModelException,
	UnknownSIdRefException, InvalidXPath,
	CannotCreateException, CannotDeleteException,

)

from .figure import SigNetSimFigure

from .LibSigNetSimException import LibSigNetSimException