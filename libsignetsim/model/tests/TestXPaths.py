#!/usr/bin/env python
""" TestXPaths.py


	Testing the XPath building and resolution


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

from libsignetsim.model.SbmlDocument import SbmlDocument
from unittest import TestCase


class TestXPaths(TestCase):
	""" Tests high level functions """

	def testResolveXPath(self):

		doc = SbmlDocument()
		model = doc.model
		model.setDefaultUnits()

		c = model.listOfCompartments.new()
		c.setName("Cell")

		s1 = model.listOfSpecies.new()
		s1.setName("Protein")

		p1 = model.listOfParameters.new()
		p1.setName("Kinetic constant")

		self.assertEqual(doc.resolveXPath("sbml:sbml/sbml:model/listOfCompartments/compartment[@name='Cell']"), c)
		self.assertEqual(doc.resolveXPath("sbml:sbml/sbml:model/listOfCompartments/compartment[@id='compartment_0']"), c)
		self.assertEqual(doc.resolveXPath("sbml:sbml/sbml:model/listOfSpecies/species[@name='Protein']"), s1)
		self.assertEqual(doc.resolveXPath("sbml:sbml/sbml:model/listOfSpecies/species[@id='species_0']"), s1)
		self.assertEqual(doc.resolveXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@name='Kinetic constant']"), p1)
		self.assertEqual(doc.resolveXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']"), p1)


		doc_comp = SbmlDocument()
		doc_comp.enableComp()

		submodel = doc_comp.listOfModelDefinitions.new()
		submodel.setSbmlId("submodel_0")
		submodel.setName("Module 0")

		sub_c = submodel.listOfCompartments.new()
		sub_c.setName("Cell")

		sub_s1 = submodel.listOfSpecies.new()
		sub_s1.setName("Protein")

		sub_p1 = submodel.listOfParameters.new()
		sub_p1.setName("Kinetic constant")

		self.assertEqual(doc_comp.resolveXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfCompartments/compartment[@name='Cell']"), sub_c)
