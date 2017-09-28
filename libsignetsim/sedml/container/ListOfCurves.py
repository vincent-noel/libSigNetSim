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

from libsignetsim.sedml.container.ListOf import ListOf
from libsignetsim.sedml.Curve import Curve
from libsignetsim.settings.Settings import Settings

class ListOfCurves(ListOf):

	def __init__(self, document, plot):

		ListOf.__init__(self, document)

		self.__document = document
		self.__plot = plot
		self.__curvesCounter = 0

	def new(self, curve_id=None):
		t_curve_id = curve_id
		if t_curve_id is None:
			t_curve_id = "%s_curve_%d" % (self.__plot.getId(), self.__curvesCounter)

		curve = Curve(self.__document)
		curve.setId(t_curve_id)
		ListOf.append(self, curve)
		self.__curvesCounter += 1
		return curve

	def createCurve(self, curve_id=None):
		return self.new(curve_id)

	def readSedml(self, list_of_curves, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_curves, level, version)

		for t_curve in list_of_curves:
			curve = Curve(self.__document)
			curve.readSedml(t_curve, level, version)
			ListOf.append(self, curve)
			self.__curvesCounter += 1

	def writeSedml(self, list_of_curves, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_curves, level, version)

		for t_curve in self:
			curve = list_of_curves.createCurve()
			t_curve.writeSedml(curve, level, version)

	def getDataToGenerate(self):

		data = []
		for curve in self:
			data += curve.getDataToGenerate()

		return list(set(data))

	def getXAxisTitle(self):

		titles = []
		for curve in self:
			titles.append(curve.getXAxisTitle())

		if len(set(titles)) == 1:
			return titles[0]

	def getYAxisTitle(self):

		titles = []
		for curve in self:
			titles.append(curve.getYAxisTitle())

		if len(set(titles)) == 1:
			return titles[0]