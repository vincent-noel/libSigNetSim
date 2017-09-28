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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.HasId import HasId
from libsignetsim.settings.Settings import Settings


class Curve(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__xDataReference = None
		self.__yDataReference = None
		self.__logX = False
		self.__logY = False

	def readSedml(self, curve, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, curve, level, version)
		HasId.readSedml(self, curve, level, version)

		if curve.isSetXDataReference():
			self.__xDataReference = curve.getXDataReference()

		if curve.isSetYDataReference():
			self.__yDataReference = curve.getYDataReference()

		if curve.isSetLogX():
			self.__logX = curve.getLogX()

		if curve.isSetLogY():
			self.__logY = curve.getLogY()

	def writeSedml(self, curve, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, curve, level, version)
		HasId.writeSedml(self, curve, level, version)

		if self.__xDataReference is not None:
			curve.setXDataReference(self.__xDataReference)

		if self.__yDataReference is not None:
			curve.setYDataReference(self.__yDataReference)

		if self.__logX is not None:
			curve.setLogX(self.__logX)

		if self.__logY is not None:
			curve.setLogY(self.__logY)

	def getXDataReference(self):
		return self.__xDataReference

	def getYDataReference(self):
		return self.__yDataReference

	def getXData(self):
		data_x = self.__document.listOfDataGenerators.getDataGenerator(self.__xDataReference)
		return data_x.getData()

	def getYData(self):
		data_y = self.__document.listOfDataGenerators.getDataGenerator(self.__yDataReference)
		return data_y.getData()

	def getData(self):
		xs = self.getXData()
		ys = self.getYData()

		data = []
		for i, x in enumerate(xs):
			data.append((x, ys[i]))
		return data

	def getLogX(self):
		return self.__logX

	def getLogY(self):
		return self.__logY

	def setXDataReference(self, x_data_reference):
		self.__xDataReference = x_data_reference

	def setXData(self, x_data):
		self.__xDataReference = x_data.getId()

	def setYDataReference(self, y_data_reference):
		self.__yDataReference = y_data_reference

	def setYData(self, y_data):
		self.__yDataReference = y_data.getId()

	def setLogX(self, log_x):
		self.__logX = log_x

	def setLogY(self, log_y):
		self.__logY = log_y

	def getDataToGenerate(self):

		return [
			self.__document.listOfDataGenerators.getDataGenerator(self.__xDataReference),
			self.__document.listOfDataGenerators.getDataGenerator(self.__yDataReference)
		]

	def build(self, fig, plot, curve_id, print_ynames):

		data_x = self.__document.listOfDataGenerators.getDataGenerator(self.__xDataReference)
		data_y = self.__document.listOfDataGenerators.getDataGenerator(self.__yDataReference)

		# print "X : %s" % str(data_x.getData())
		# print "Y : %s" % str(data_y.getData())
		if not print_ynames:
			fig.plot(plot, curve_id, data_x.getData(), data_y.getData())
		else:
			fig.plot(plot, curve_id, data_x.getData(), data_y.getData(), y_name=self.getYAxisTitle())


	def getXAxisTitle(self):
		return self.__document.listOfDataGenerators.getDataGenerator(self.__xDataReference).getName()

	def getYAxisTitle(self):
		return self.__document.listOfDataGenerators.getDataGenerator(self.__yDataReference).getName()

