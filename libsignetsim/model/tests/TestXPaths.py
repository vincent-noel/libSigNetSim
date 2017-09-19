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
from libsignetsim.model.sbml.KineticLaw import KineticLaw

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

		p1 = model.listOfParameters.new(value=42)
		p1.setName("Kinetic constant")

		r1 = model.listOfReactions.new()
		r1.setName("Protein degradation")
		r1.listOfReactants.add(s1)
		r1.setKineticLaw(KineticLaw.MASS_ACTION, reversible=False, parameters=[p1])

		e1 = model.listOfEvents.new()
		e1.setName("Reaction stop")
		e1.setTrigger("reaction_0 > 1")
		e1.addEventAssignment(p1, 0)

		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfCompartments/compartment[@name='Cell']"), c)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfCompartments/compartment[@id='compartment_0']"), c)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfCompartments/compartment[@id='compartment_0']/@size"), 1)

		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfSpecies/species[@name='Protein']"), s1)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfSpecies/species[@id='species_0']"), s1)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfSpecies/species[@id='species_0']/@value"), 0)

		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@name='Kinetic constant']"), p1)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']"), p1)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@value"), 42)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@name"), "Kinetic constant")
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@id"), "parameter_0")

		doc.setByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@value", 51)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@value"), 51)
		doc.setByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@name", "Degradation constant")
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@name"), "Degradation constant")
		doc.setByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='parameter_0']/@id", "kdeg")
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfParameters/parameter[@id='kdeg']/@id"), "kdeg")

		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfReactions/reaction[@name='Protein degradation']"), r1)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfReactions/reaction[@id='reaction_0']"), r1)

		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfEvents/event[@name='Reaction stop']"), e1)
		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/listOfEvents/event[@id='event_0']"), e1)

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

		self.assertEqual(doc_comp.getByXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfCompartments/compartment[@name='Cell']"), sub_c)
		self.assertEqual(doc_comp.getByXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfCompartments/compartment[@id='compartment_0']"), sub_c)
		self.assertEqual(doc_comp.getByXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfSpecies/species[@name='Protein']"), sub_s1)
		self.assertEqual(doc_comp.getByXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfSpecies/species[@id='species_0']"), sub_s1)
		self.assertEqual(doc_comp.getByXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfParameters/parameter[@name='Kinetic constant']"), sub_p1)
		self.assertEqual(doc_comp.getByXPath("sbml:sbml/sbml:listOfModelDefinitions/modelDefinition[@id='submodel_0']/listOfParameters/parameter[@id='parameter_0']"), sub_p1)

		self.assertEqual(doc.getByXPath("sbml:sbml/sbml:model/descendant::*[@id='species_0']"), s1)
		self.assertEqual(s1.getXPath(), "sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='species_0']")
		self.assertEqual(s1.getXPath("value"), "sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='species_0']/@value")
