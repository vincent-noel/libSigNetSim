#!/usr/bin/env python
""" SbmlMathReader.py


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


import libsbml
from math import isinf, isnan
from sympy import srepr
from libsignetsim.model.math.sympy_shortcuts import *
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import ModelException


class SbmlMathReader(object):
	""" Class for handling math formulaes """


	def __init__(self, model):
		""" Constructor """

		self.model = model


	def readSbml(self, formula, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Import a math formula from sbml """

		self.sbmlLevel = sbml_level
		self.sbmlVersion = sbml_version

		self.internalTree = self.translateForInternal(formula, sbml_level, sbml_version)

		# if self.isKineticLaw:
		#     self.simplifiedInternalTree = self.translateForDeveloppedInternal(self.translateForInternal(formula, sbml_level, sbml_version, True))
		#     self.simplifiedInternalTree_v2 = self.translateForDeveloppedInternal(self.translateForInternal(formula, sbml_level, sbml_version, False, False))

		if Settings.verbose >= 2:
			print "\n> readSbml : "
			print ">> input : %s" % self.printSbml(formula)
			print ">> output simplified : %s" % str(self.internalTree)
			print ">> output : %s" % srepr(self.internalTree)

	def printSbml(self, formula, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if isinstance(formula, str):
			return formula
		elif isinstance(formula, libsbml.ASTNode):
			if sbml_level <= 2:
				return libsbml.formulaToString(formula)
			else:
				return libsbml.formulaToL3String(formula)
		else:
			return str(formula)


	def translateVariableForInternal(self, variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion, simplified=False, develop=True):

		# Local parameter
		# If we are within a reaction, we first need to look in the local
		# scope for the variable identifier
		#TODO this is called three timed at initialization ??!!
		# because of the tree versions of the tree (normal, simplified 1 & 2)

		#print "translate variable for interal : %s" % str(variable)

		if self.isFromReaction is not None and self.model.listOfReactions[self.isFromReaction].listOfLocalParameters.containsSbmlId(variable):
			if simplified:
				return SympySymbol("_parameter_")
			else:
				return self.model.listOfReactions[self.isFromReaction].listOfLocalParameters.getBySbmlId(variable).symbol.getInternalMathFormula()


		# And if we are within a function definition, we will encounter
		# variables which are only local
		elif self.isFunctionDefinition:
			return SympySymbol(variable)

		# print self.model.listOfVariables.keys()
		# Finally, we look in our list of variables
		elif variable in self.model.listOfVariables.keys():

			t_variable = self.model.listOfVariables[variable]

			# If the symbol is not yet initialized,
			# then it's our job
			if t_variable.symbol.getInternalMathFormula() is None:
				return SympySymbol(variable)

			elif t_variable.isStoichiometry():
				if simplified:
					return SympyInteger(1)
				else:
					return t_variable.symbol.getInternalMathFormula()

			elif t_variable.isCompartment():
				if simplified:
					return SympyInteger(1)
				else:
					return t_variable.symbol.getInternalMathFormula()

			elif t_variable.isParameter():
				if simplified:
					return SympySymbol("_parameter_")
				else:
					return t_variable.symbol.getInternalMathFormula()

			elif t_variable.isReaction():
				if simplified:
					return SympySymbol("_reaction_")
				else:
					return t_variable.symbol.getInternalMathFormula()

			elif t_variable.isSpecies():
				if simplified:
					return SympySymbol("_species_")

				elif not develop:
					return t_variable.symbol.getInternalMathFormula()

				elif (self.isKineticLaw
						or self.isRateRule
						or self.isEquation
						or self.isEventAssignment
						or self.isAssignmentRule
						or self.isAlgebraicRule):

					# If the species represents a concentration
					# We should make it corresponds to amount/size
					if t_variable.isConcentration():

						return SympySymbol("_speciesForcedConcentration_%s_"
											% str(t_variable.symbol.getInternalMathFormula()))

					# Otherwise we use amount
					else:
						return t_variable.symbol.getInternalMathFormula()

				else:
					return t_variable.symbol.getInternalMathFormula()

			else:
				raise ModelException(ModelException.SBML_ERROR,
						"Unknown type of variable : %s" % variable)

		elif variable == "_time_":
			return SympySymbol("_time_")

		else:
			raise ModelException(ModelException.SBML_ERROR,
					"Unknown variable : %s" % variable)


	def translateForInternal(self, tree, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion, simplified=False, develop=True):
		""" Translate an SBML Tree in a Sympy Tree """


		if tree is None or tree == 0:
			return SympyInteger(0)

		elif isinstance(tree,int):
			return SympyInteger(tree)

		elif isinstance(tree, float):
			if isinf(tree):
				if tree > 0:
					return SympyInf
				else:
					return SympyMul(SympyInteger(-1), SympyInf)

			elif isnan(tree):
				return SympyNan

			return SympyFloat(tree)

		elif isinstance(tree, str):
			return self.translateVariableForInternal(tree, sbml_level, sbml_version, simplified, develop)

		# print libsbml.formulaToString(tree)

		if tree.isInfinity():
			return SympyInf

		elif tree.isNegInfinity():
			return SympyMul(SympyInteger(-1), SympyInf)

		elif tree.isNaN():
			return SympyNan

		elif tree.getType() == libsbml.AST_RATIONAL:
			return SympyRational(SympyInteger(tree.getNumerator()), SympyInteger(tree.getDenominator()))


		elif tree.isNumber():

			if tree.isInteger():
				return SympyInteger(tree.getInteger())

			elif tree.isReal():
				return SympyFloat(tree.getReal())

			elif tree.getType() == libsbml.AST_REAL_E:
				return SympyE

			else:
				raise ModelException(ModelException.SBML_ERROR,
											"Number error")


		elif tree.isConstant():
			if tree.getType() == libsbml.AST_CONSTANT_E:
				return SympyE

			elif tree.getType() == libsbml.AST_CONSTANT_FALSE:
				return False

			elif tree.getType() == libsbml.AST_CONSTANT_TRUE:
				return True

			elif tree.getType() == libsbml.AST_CONSTANT_PI:
				# print " PIIIIIII"
				return SympyPi

			elif tree.getType() == libsbml.AST_NAME_AVOGADRO or tree.getType() == libsbml.AST_TYPECODE_CSYMBOL_AVOGADRO:
				# print " Avogadro detected"
				return SympySymbol("_avogadro_")

			else:
				raise ModelException(ModelException.SBML_ERROR,
							"Unknown constant")

		elif tree.isOperator():

			if tree.getType() == libsbml.AST_PLUS:
				# print libsbml.formulaToString(tree)
				if tree.getNumChildren() == 2:
					return SympyAdd(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
									self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)
				elif tree.getNumChildren() == 1:
					return self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop)

				elif tree.getNumChildren() == 0:
					return SympyInteger(0)

				else:
					t_tree = SympyAdd(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
										self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)
					for i_arg in range(2,tree.getNumChildren()):
						t_tree = SympyAdd(t_tree, self.translateForInternal(tree.getChild(i_arg), sbml_level, sbml_version, simplified, develop), evaluate=False)

					return t_tree


			elif tree.getType() == libsbml.AST_MINUS:

				if tree.getNumChildren() == 2:
					return SympyAdd(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
									SympyMul(SympyInteger(-1),self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False), evaluate=False)

				elif tree.getNumChildren() == 1:
					return SympyMul(SympyInteger(-1),
									self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				elif tree.getNumChildren() == 0:
					return SympyInteger(0)

				else:
					return SympySymbol("ERR_MINUS_TERNARY")


			elif tree.getType() == libsbml.AST_TIMES:


				if tree.getNumChildren() == 2:
					return SympyMul(
							self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
							self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False
					)

				elif tree.getNumChildren() == 1:
					return self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop)

				elif tree.getNumChildren() == 0:
					return SympyInteger(1)
				else:
					t_tree = SympyMul(
								self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
								self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False
					)

					for i_arg in range(2,tree.getNumChildren()):
						t_tree = SympyMul(t_tree, self.translateForInternal(tree.getChild(i_arg), sbml_level, sbml_version, simplified, develop), evaluate=False)

					return t_tree

			elif tree.getType() == libsbml.AST_DIVIDE:
				if tree.getChild(0).isNumber() and tree.getChild(1).isNumber():

					t_tree = SympyRational(
						SympyInteger(self.translateForInternal(tree.getChild(0), simplified, develop)),
						SympyInteger(self.translateForInternal(tree.getChild(1), simplified, develop)))

					return t_tree

				else:
					return SympyMul(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
								SympyPow(self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), SympyInteger(-1)))

			elif tree.getType() == libsbml.AST_POWER:
				t_x = self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop)
				t_n = self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop)
				return SympyPow(t_x, t_n, evaluate=False)


		elif tree.isFunction():

				# AST_FUNCTION_ABS
			if tree.getType() == libsbml.AST_FUNCTION_ABS:
				return SympyAbs(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCCOS
			elif tree.getType() == libsbml.AST_FUNCTION_ARCCOS:
				return SympyAcos(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCCOSH
			elif tree.getType() == libsbml.AST_FUNCTION_ARCCOSH:
				return SympyAcosh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCCOT
			elif tree.getType() == libsbml.AST_FUNCTION_ARCCOT:
				return SympyAcot(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCCOTH
			elif tree.getType() == libsbml.AST_FUNCTION_ARCCOTH:
				return SympyAcoth(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCCSC
			elif tree.getType() == libsbml.AST_FUNCTION_ARCCSC:
				return SympyAcsc(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCCSCH
			elif tree.getType() == libsbml.AST_FUNCTION_ARCCSCH:
				return SympyAsinh(SympyPow(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), SympyInteger(-1), evaluate=False), evaluate=False)

				# AST_FUNCTION_ARCSEC
			elif tree.getType() == libsbml.AST_FUNCTION_ARCSEC:
				return SympyAsec(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCSECH
			elif tree.getType() == libsbml.AST_FUNCTION_ARCSECH:
				return SympyAcosh(SympyPow(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), SympyInteger(-1), evaluate=False), evaluate=False)

				# AST_FUNCTION_ARCSIN
			elif tree.getType() == libsbml.AST_FUNCTION_ARCSIN:
				return SympyAsin(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCSINH
			elif tree.getType() == libsbml.AST_FUNCTION_ARCSINH:
				return SympyAsinh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCTAN
			elif tree.getType() == libsbml.AST_FUNCTION_ARCTAN:
				return SympyAtan(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_ARCTANH
			elif tree.getType() == libsbml.AST_FUNCTION_ARCTANH:
				return SympyAtanh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_CEILING
			elif tree.getType() == libsbml.AST_FUNCTION_CEILING:
				return SympyCeiling(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_COS
			elif tree.getType() == libsbml.AST_FUNCTION_COS:
				return SympyCos(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_COSH
			elif tree.getType() == libsbml.AST_FUNCTION_COSH:
				return SympyCosh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_COT
			elif tree.getType() == libsbml.AST_FUNCTION_COT:
				return SympyCot(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_COTH
			elif tree.getType() == libsbml.AST_FUNCTION_COTH:
				return SympyCoth(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_CSC
			elif tree.getType() == libsbml.AST_FUNCTION_CSC:
				return SympyCsc(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_CSCH
			elif tree.getType() == libsbml.AST_FUNCTION_CSCH:
				# return SympyCsch(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)
				return SympyPow(SympySinh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False),
								SympyInteger(-1), evaluate=False)
				# AST_FUNCTION_DELAY
			elif tree.getType() == libsbml.AST_FUNCTION_DELAY:
				return SympyFunction("_delay_")(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
												self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop))

				# AST_FUNCTION_EXP
			elif tree.getType() == libsbml.AST_FUNCTION_EXP:
				return SympyExp(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_FACTORIAL
			elif tree.getType() == libsbml.AST_FUNCTION_FACTORIAL:
				return SympyFactorial(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_FLOOR
			elif tree.getType() == libsbml.AST_FUNCTION_FLOOR:
				return SympyFloor(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_LN
			elif tree.getType() == libsbml.AST_FUNCTION_LN:
				return SympyLog(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_LOG
			elif tree.getType() == libsbml.AST_FUNCTION_LOG:
				t_n = self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop)
				t_x = self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop)

				return SympyLog(t_x, t_n, evaluate=False)

				# AST_FUNCTION_PIECEWISE
			elif tree.getType() == libsbml.AST_FUNCTION_PIECEWISE:
				i_arg = 0
				i_cond = 0
				t_pieces = []



				while i_arg < tree.getNumChildren():

					if (i_arg+1) < tree.getNumChildren():
						# print "here we have a full condition"
						t_value = self.translateForInternal(tree.getChild(i_arg), sbml_level, sbml_version, simplified, develop)
						t_condition = self.translateForInternal(tree.getChild(i_arg+1), sbml_level, sbml_version, simplified, develop)
						t_pieces.append((t_value, t_condition))
						# print t_value
						# print t_condition
						i_arg += 2
					else:
						# print "and there we have the else"
						t_value = self.translateForInternal(tree.getChild(i_arg), sbml_level, sbml_version, simplified, develop)
						t_pieces.append((t_value, True))
						i_arg += 1

				# print "\n> Result :"
				# print t_pieces
				# print *(t_pieces)

				return SympyPiecewise(*t_pieces, evaluate=False)


				# AST_FUNCTION_POWER
			elif tree.getType() == libsbml.AST_FUNCTION_POWER:
				t_x = self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop)
				t_n = self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop)
				return SympyPow(t_x, t_n, evaluate=False)

				# AST_FUNCTION_ROOT
			elif tree.getType() == libsbml.AST_FUNCTION_ROOT:
				return SympyPow(self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop),
								SympyPow(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), SympyInteger(-1), evaluate=False), evaluate=False)

				# AST_FUNCTION_SEC
			elif tree.getType() == libsbml.AST_FUNCTION_SEC:
				return SympySec(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_SECH
			elif tree.getType() == libsbml.AST_FUNCTION_SECH:
				return SympyPow(SympyCosh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False), SympyInteger(-1), evaluate=False)

				# AST_FUNCTION_SIN
			elif tree.getType() == libsbml.AST_FUNCTION_SIN:
				return SympySin(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_SINH
			elif tree.getType() == libsbml.AST_FUNCTION_SINH:
				return SympySinh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_TAN
			elif tree.getType() == libsbml.AST_FUNCTION_TAN:
				return SympyTan(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

				# AST_FUNCTION_TANH
			elif tree.getType() == libsbml.AST_FUNCTION_TANH:
				return SympyTanh(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)


			else:
				t_args = []
				for param in range(0, tree.getNumChildren()):
					t_args.append(self.translateForInternal(tree.getChild(param), sbml_level, sbml_version, simplified, develop))

				t_funcdef = self.model.listOfFunctionDefinitions.getBySbmlId(tree.getName())
				t_name = "_functionDefinition_%d_" % (t_funcdef.objId)
				t_function = SympyFunction(t_name)(*t_args)

				return t_function


		elif tree.getType() == libsbml.AST_LAMBDA:

			t_args = []
			for param in range(0, tree.getNumChildren()-1):
				t_args.append(self.translateForInternal(tree.getChild(param), sbml_level, sbml_version, simplified, develop))

			t_def = self.translateForInternal(tree.getChild(tree.getNumChildren()-1), sbml_level, sbml_version, simplified, develop)

			return SympyLambda(tuple(t_args), t_def)


		elif tree.isRelational():

			if tree.getType() == libsbml.AST_RELATIONAL_EQ:
				return SympyEqual(
						self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
						self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)

			elif tree.getType() == libsbml.AST_RELATIONAL_NEQ:
				return SympyUnequal(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
									self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)

			elif tree.getType() == libsbml.AST_RELATIONAL_GT:
				return SympyStrictGreaterThan(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
												self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)

			elif tree.getType() == libsbml.AST_RELATIONAL_LT:
				return SympyStrictLessThan(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
											self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)

			elif tree.getType() == libsbml.AST_RELATIONAL_GEQ:
				return SympyGreaterThan(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
										self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)

			elif tree.getType() == libsbml.AST_RELATIONAL_LEQ:
				return SympyLessThan(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop),
										self.translateForInternal(tree.getChild(1), sbml_level, sbml_version, simplified, develop), evaluate=False)

			else:
				raise ModelException(ModelException.SBML_ERROR, "Unknown relational operator")
				return SympySymbol("ERR_RELATIONAL")


		elif tree.isLogical():

			if tree.getType() == libsbml.AST_LOGICAL_AND:
				t_children = []
				for child in range(0, tree.getNumChildren()):
					t_children.append(self.translateForInternal(tree.getChild(child), sbml_level, sbml_version, simplified, develop))

				return SympyAnd(*t_children, evaluate=False)

			elif tree.getType() == libsbml.AST_LOGICAL_OR:
				t_children = []
				for child in range(0, tree.getNumChildren()):
					t_children.append(self.translateForInternal(tree.getChild(child), sbml_level, sbml_version, simplified, develop))

				return SympyOr(*t_children, evaluate=False)

			elif tree.getType() == libsbml.AST_LOGICAL_XOR:
				t_children = []
				for child in range(0, tree.getNumChildren()):
					t_children.append(self.translateForInternal(tree.getChild(child), sbml_level, sbml_version, simplified, develop))

				return SympyXor(*t_children, evaluate=False)

			elif tree.getType() == libsbml.AST_LOGICAL_NOT:
				return SympyNot(self.translateForInternal(tree.getChild(0), sbml_level, sbml_version, simplified, develop), evaluate=False)

			else:
				raise ModelException(ModelException.SBML_ERROR, "Unknown logical operator")
				return "unknown logical operator"


		elif tree.getType() == libsbml.AST_NAME:
			return self.translateVariableForInternal(tree.getName(), sbml_level, sbml_version, simplified, develop)

		elif tree.getType() == libsbml.AST_NAME_TIME:
			return SympySymbol("_time_")

		elif tree.getType() == libsbml.AST_NAME_AVOGADRO or tree.getType() == libsbml.AST_TYPECODE_CSYMBOL_AVOGADRO:
			print "Avogadro detected 2"
			return SympySymbol("_avogadro_")

		else:
			if sbml_level <= 2:
				t_string = libsbml.formulaToString(tree)
			else:
				t_string = libsbml.formulaToL3String(tree)

			raise ModelException(ModelException.SBML_ERROR, "Unknown mathematical term : %s" % t_string)

			return SympySymbol("ERR_UNKNOWN_TYPE")
