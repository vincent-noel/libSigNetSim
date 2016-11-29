#!/usr/bin/env python
""" SbmlExternalDocument.py


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

# import signetsim.model


from libsignetsim.model.Model import Model

from libsignetsim.model.Variable import Variable
from libsignetsim.model.ModelInstance import ModelInstance
from libsignetsim.model.ModelException import ModelException
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.SbmlDocument import SbmlDocument


class SbmlExternalDocument(SbmlDocument):
    """ Sbml model class """


    def __init__ (self, path):
        """ Constructor of model class """

        SbmlDocument.__init__(self, path=path)

    def readSbml(self, sbmlFilename):

        SbmlDocument.readSbml(self, sbmlFilename)

    def writeSbml(self, sbml_filename):

        SbmlDocument.writeSbml(self, sbmlFilename)

    def getModelInstance(self):

        return SbmlDocument.getModelInstance(self)