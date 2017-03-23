#!/usr/bin/env python
""" ListOfCurves.py


	This file ...


	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.Curve import Curve
from libsignetsim.settings.Settings import Settings

class ListOfCurves(SedBase):

	def __init__(self, document):

		SedBase.__init__(self, document)

		self.__document = document
		self.listOfCurves = []


	def readSedml(self, list_of_curves, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, list_of_curves, level, version)

		for t_curve in list_of_curves:
			curve = Curve(self.__document)
			curve.readSedml(t_curve, level, version)
			self.listOfCurves.append(curve)
