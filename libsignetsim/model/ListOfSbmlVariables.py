#!/usr/bin/env python
""" ListOfSbmlVariables.py


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


from re import sub

from libsignetsim.model.sbml.SbmlVariable import SbmlVariable

class ListOfSbmlVariables(object):
	""" Parent class for all the ListOf_ containers in a sbml model """

	def __init__ (self, model):

		self.__model = model

	#
	# def remove(self, variable):
	#     del self.listOfVariables[variable.getSbmlId()]


	def containsName(self, name):
		""" Test if a name is in the list """

		for obj in dict.values(self):
			if name == obj.getName():
				return True
		return False


	def getByName(self, name, pos=0):
		""" Find sbml objects by their name """
		return [obj for obj in dict.values(self) if obj.getName() == name][pos]

	def containsSbmlId(self, sbml_id):
		for var in dict.values(self):
			# We have a risk of conflict with local parameters, who have a special scope. So we just ignore them here
			if var.getSbmlId() == sbml_id and not (var.isParameter() and var.isLocalParameter()):
				return True
		return False

	def getBySbmlId(self, sbml_id):
		for var in dict.values(self):
			# We have a risk of conflict with local parameters, who have a special scope. So we just ignore them here
			if var.getSbmlId() == sbml_id and not (var.isParameter() and var.isLocalParameter()):
				return var

	def newSbmlId(self, variable, string=None):

		# If the string is empty, we choose the type of object as a root
		t_string = None
		if string == None:
			if variable.isSpecies():
				t_string = "species_%d" % variable.objId

			elif variable.isCompartment():
				t_string = "compartment_%d" % variable.objId

			elif variable.isReaction():
				t_string = "reaction_%d" % variable.objId

			elif variable.isParameter():
				if variable.isLocalParameter():
					t_string = "_local_%d_parameter_%d" % (variable.reaction.objId, variable.objId)
				else:
					t_string = "parameter_%d" % variable.objId

		# Otherwise we force the restriction on the string
		else:
			t_string = sub('[ ]+','_', string)
			t_string = sub('[^A-Za-z0-9_]+', '', t_string)

		# We check if the sbmlId already exist, and if so we add numbers !
		# THIS SUCKS
		if t_string in dict.keys(self):
			i = 1
			while ("%s_%d" % (t_string, i)) in dict.keys(self):
				i += 1
			t_string = "%s_%d" % (t_string, i)

		return t_string
