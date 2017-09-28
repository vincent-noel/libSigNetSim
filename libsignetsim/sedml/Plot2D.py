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

	This file ...

"""

from libsignetsim.sedml.Output import Output
from libsignetsim.sedml.container.ListOfCurves import ListOfCurves
from libsignetsim.figure.SigNetSimFigure import SigNetSimFigure
from libsignetsim.settings.Settings import Settings


class Plot2D(Output):

	def __init__(self, document):

		Output.__init__(self, document)

		self.__document = document
		self.listOfCurves = ListOfCurves(self.__document, self)

	def readSedml(self, plot, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Output.readSedml(self, plot, level, version)
		self.listOfCurves.readSedml(plot.getListOfCurves(), level, version)

	def writeSedml(self, plot, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Output.writeSedml(self, plot, level, version)
		self.listOfCurves.writeSedml(plot.getListOfCurves(), level, version)

	def showFigure(self):
		fig = SigNetSimFigure()
		subplot = fig.add_subplot(1,1,1)

		print_ynames = False
		if self.listOfCurves.getXAxisTitle() is not None:
			subplot.set_xlabel(self.listOfCurves.getXAxisTitle())

		if self.listOfCurves.getYAxisTitle() is not None:
			subplot.set_ylabel(self.listOfCurves.getYAxisTitle())
		else:
			print_ynames = True

		for i, curve in enumerate(self.listOfCurves):
			curve.build(fig, subplot, i, print_ynames)

		if print_ynames:
			subplot.legend(loc='upper right')

		subplot.set_title(self.getName())


	def getDataToGenerate(self):

		return self.listOfCurves.getDataToGenerate()

