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

	This file is made for 'high level' tests, using various components

"""

from builtins import range
from libsignetsim import Model, SbmlDocument, TimeseriesSimulation, Settings
from unittest import TestCase
from os.path import exists, join, dirname


class TestTimeseries(TestCase):
	""" Tests high level functions """

	def __buildMichaelisModel(self):

		m = Model()
		m.setName("Enzymatic Reaction")

		e = m.listOfSpecies.new("E")
		s = m.listOfSpecies.new("S")
		p = m.listOfSpecies.new("P")

		vmax = m.listOfParameters.new("vmax")
		km = m.listOfParameters.new("km")

		r = m.listOfReactions.new("Enzymatic reaction")
		r.listOfReactants.add(s)
		r.listOfModifiers.add(e)
		r.listOfProducts.add(p)
		r.kineticLaw.setPrettyPrintMathFormula("vmax*E*S/(km+S)", forcedConcentration=True)

		e.setValue(10)
		s.setValue(12)
		p.setValue(0)
		vmax.setValue(0.211)
		km.setValue(1.233)

		return m


	def testSimulateMichaelisMenten(self):

		reference_data = [0.0, 1.897738187453314, 3.756955433409792, 5.562177924708521, 7.287504219961273,
						  8.886453435701496, 10.27109268766486, 11.28772309320835, 11.80437071324164,
						  11.95991226988507, 11.99256438900284, 11.99865019516933, 11.9997559549625,
						  11.99995590896604, 11.99999203526398, 11.99999856126113, 11.99999974010935,
						  11.99999995305381, 11.99999999151893, 11.99999999846709, 11.99999999972277]

		m = self.__buildMichaelisModel()

		sim = TimeseriesSimulation([m], time_min=0, time_ech=1, time_max=20)
		sim.run()
		_,y = sim.getRawData()[0]
		model_data = y['P']

		for i, t_data in enumerate(reference_data):
			self.assertAlmostEqual(t_data, model_data[i], delta=1e-4)

		# Running just to see if it fails
		sim.plot()

	def testZeroResults(self):

		reference_data = [0.0, 1.897738187453314, 3.756955433409792, 5.562177924708521, 7.287504219961273,
						  8.886453435701496, 10.27109268766486, 11.28772309320835, 11.80437071324164,
						  11.95991226988507, 11.99256438900284, 11.99865019516933, 11.9997559549625,
						  11.99995590896604, 11.99999203526398, 11.99999856126113, 11.99999974010935,
						  11.99999995305381, 11.99999999151893, 11.99999999846709, 11.99999999972277]

		m = self.__buildMichaelisModel()

		sim = TimeseriesSimulation([m], time_min=0, list_samples=list(range(0,21)))
		sim.run()
		_,y = sim.getRawData()[0]
		model_data = y['P']

		for i, t_data in enumerate(reference_data):
			self.assertAlmostEqual(t_data, model_data[i], delta=1e-4)


	def testNonzeroResult(self):
		""" Here we test a simulation which starts at zero, but the sample list doesn't include it """

		reference_data = [1.897738187453314, 3.756955433409792, 5.562177924708521, 7.287504219961273,
						  8.886453435701496, 10.27109268766486, 11.28772309320835, 11.80437071324164,
						  11.95991226988507, 11.99256438900284, 11.99865019516933, 11.9997559549625,
						  11.99995590896604, 11.99999203526398, 11.99999856126113, 11.99999974010935,
						  11.99999995305381, 11.99999999151893, 11.99999999846709, 11.99999999972277]

		m = self.__buildMichaelisModel()

		sim = TimeseriesSimulation([m], time_min=0, list_samples=list(range(1,21)))
		sim.run()
		_,y = sim.getRawData()[0]

		model_data = y['P']

		for i, t_data in enumerate(reference_data):
			self.assertAlmostEqual(t_data, model_data[i], delta=1e-4)



	def testCellCycle(self):

		sbml_path = join(dirname(__file__), "models", "modelXZknew.xml")
		self.assertTrue(exists(sbml_path))

		doc = SbmlDocument()
		doc.readSbmlFromFile(sbml_path)
		model = doc.getModelInstance()

		sim = TimeseriesSimulation([model], time_min=0, time_ech=1, time_max=100)
		sim.run()
		t, y = sim.getRawData()[0]

		reference_data = {
			'Me' : [0.01, 0.003580233457277267, 0.002373903298493611, 0.002154579921145382, 0.002127212898745217, 0.002127484739029041, 0.002137257005830825, 0.002162145586296829, 0.002212273709778234, 0.002307542790554124, 0.002486827612636255, 0.002832801257929566, 0.00355212385189969, 0.005360425502991762, 0.01566019704784742, 0.1047110528094425, 0.1954260599664658, 0.2926292082359158, 0.376194881427533, 0.4409162312471451, 0.4846280391270638, 0.4373580894876331, 0.3817842632611382, 0.3275265887034692, 0.2756539704362985, 0.2268241046614763, 0.1817078514873129, 0.1410608549817309, 0.105695532707276, 0.07640163485781036, 0.05567932170574095, 0.04056579725412696, 0.02854747273887125, 0.01928165268065314, 0.01169421469998987, 0.004397579057233, 0.001901806531359242, 0.001827453825061841, 0.008915781959284741, 0.09880055289416922, 0.1763489219281542, 0.2202904866680906, 0.2520159272611591, 0.2781987543114496, 0.3003906181403596, 0.3188001388628576, 0.3334537621989606, 0.3442345818645767, 0.3501630787639504, 0.3153929609127216, 0.2649546862207008, 0.2169912696571441, 0.1727736500115944, 0.1331727233115165, 0.09902053765127497, 0.07106957940833458, 0.05204783447458349, 0.03755228613113723, 0.02621694241975501, 0.01744316214163091, 0.009948478965563426, 0.003282347860028406, 0.001755325234051864, 0.003816282522790071, 0.01594026985361677, 0.1262034443249798, 0.1854771314737674, 0.221439511344644, 0.2480667109322641, 0.2703059093058452, 0.2891611943281227, 0.3046823145608167, 0.316769263201209, 0.3250205291880593, 0.3167871855710658, 0.2677214152070742, 0.2197440575287281, 0.1753070247952546, 0.1354087748962449, 0.1009047679735218, 0.07256229511992084, 0.05289779983630954, 0.03826776927971698, 0.02676347579369785, 0.01786577488360008, 0.01033902398417713, 0.003470651418676291, 0.001770294253218754, 0.003597809636599793, 0.01435924789225343, 0.1214485695217362, 0.1815153510695385, 0.2172703975860132, 0.2432862899662414, 0.2649269644559726, 0.2833499329907692, 0.2985956076256834, 0.310540238196016, 0.3187847137354839, 0.3125067457294482, 0.2639026873410995],
			'Ma' : [0.01, 0.004657255728410925, 0.003734108543244096, 0.003430388355261345, 0.0033916416659306, 0.003406951686092824, 0.003430511045354618, 0.003465552124596455, 0.003521917563182068, 0.003617281100109027, 0.003784657609051174, 0.00409058632302915, 0.004687539979874434, 0.006019732353186567, 0.01063071796629902, 0.02360968592555503, 0.03685990799760419, 0.04939244687637789, 0.05104449326467021, 0.0572741870045799, 0.2584440234037855, 0.4524047245171942, 0.4708813692334321, 0.4582377421476101, 0.4393768195413853, 0.4194756187205338, 0.3995338381129276, 0.3795360242665042, 0.359115559559967, 0.337320949186558, 0.3218422038005405, 0.2551084786795799, 0.1852422243494423, 0.1143990941935261, 0.03861100439095868, 0.01121600573498786, 0.004799216387534913, 0.006049119406373079, 0.01011649931943023, 0.02740619271356917, 0.03813265559473723, 0.03962711286255165, 0.03473346402022192, 0.03479317191812671, 0.03746580639447061, 0.04119719241347757, 0.04604238754264686, 0.05401579749839767, 0.1069487399777443, 0.4015458943979204, 0.4246257890560807, 0.4141984314421416, 0.3970627950139126, 0.3780900305639475, 0.3580305946317388, 0.335940754141499, 0.3165036864940237, 0.2467890554469554, 0.1764468641698983, 0.1042878529824538, 0.03078141407015968, 0.009354624506356287, 0.005110896775207856, 0.006924386771596255, 0.01363967785508944, 0.03209968396083905, 0.04224947927669164, 0.04187072884748436, 0.03649250796884101, 0.03689175316568651, 0.03975278712797207, 0.04380098517895997, 0.04962547016052436, 0.06355152127407922, 0.3374735557927575, 0.416984962783701, 0.4159559891380623, 0.4009550163601879, 0.3825675587585426, 0.3627129354822565, 0.3408354990395772, 0.3239811669082813, 0.2548869716355875, 0.184206291872803, 0.1121641178302855, 0.03582351075022085, 0.01029997252879917, 0.005241803950635648, 0.006926167049150753, 0.01316689372406677, 0.03183769759604503, 0.04271018187243411, 0.04347657667391192, 0.0372425781195675, 0.03709666333053491, 0.03978025125430098, 0.04373052404135935, 0.04941561436373471, 0.0625357968781473, 0.3286959862293812, 0.4149460425458881],
			'Mb' : [0.01, 0.007141195381161781, 0.006341459616068162, 0.006116829690953466, 0.006163542940576367, 0.006257478887571848, 0.006334632705216821, 0.006388303491398567, 0.006425929160922065, 0.006456960581941072, 0.006491476783021137, 0.006543337715940336, 0.006640550624874139, 0.006868498654370442, 0.007789213001799716, 0.008124083797483726, 0.007167811149030266, 0.006466319478929198, 0.006079986544706992, 0.005988271356957365, 0.006027584709290142, 0.02023679576153008, 0.02534974587453531, 0.02716993252315515, 0.02808506760125685, 0.02866039382018038, 0.02911049533504457, 0.029650029543183, 0.03104659794683353, 0.03688390860467454, 0.4060654150398815, 0.4317085231613322, 0.4198695949442024, 0.3948068422918858, 0.3388520929479434, 0.1885706573981542, 0.05723301507349798, 0.02863881159660372, 0.02775836948733174, 0.03151259992535529, 0.02125023151568053, 0.01337880072695647, 0.008848060918208068, 0.006983797586301386, 0.006314136605825374, 0.006085017205042112, 0.006008625950337429, 0.00598473630040011, 0.005982879305942329, 0.01757399929827213, 0.02457081409867136, 0.02688064153306522, 0.02803795571527843, 0.02899715034086099, 0.03097127383661918, 0.03845605776599642, 0.4213982415679507, 0.4287462083882658, 0.4145262404223866, 0.384974323298489, 0.3141123139364772, 0.147560897094386, 0.03432026183567985, 0.02466632888850389, 0.0242505404577476, 0.02072924809710293, 0.01313423082141208, 0.00863717176662175, 0.006823146078300861, 0.00624035878068658, 0.006057620999337455, 0.005999364943804556, 0.005981383938509569, 0.005978098053759199, 0.009423904418013277, 0.02221840218724957, 0.02601083712182449, 0.02758700531101622, 0.02868608448375215, 0.03058430563506323, 0.0373866043986767, 0.4102720802504323, 0.4288402701799299, 0.4153753065746084, 0.3869476328584468, 0.3198124170215242, 0.1552216820980901, 0.03552268937012162, 0.0241270452540637, 0.0229858771132215, 0.0197725798212933, 0.01252160506384138, 0.008386406973391304, 0.006731236002486317, 0.006206740302803208, 0.006046041041947806, 0.005995666175873651, 0.005980330160910322, 0.00597780770704834, 0.008706399681580655, 0.02196722918181939],
			'Md' : [0.01, 0.04115294265086863, 0.03561781650022201, 0.03518163614010397, 0.03679505800314324, 0.0387981923204227, 0.04062796695033716, 0.04218208259876283, 0.04352263454323368, 0.04479086360165357, 0.0462185150312336, 0.04824101825255674, 0.05192796897867308, 0.0613132638339493, 0.1276755407567878, 0.7380314583764096, 1.052497986140105, 1.195615457255023, 1.261071736375011, 1.290748054835791, 1.303982698011543, 1.308069952597923, 1.306148482750825, 1.3010044005377, 1.29357006603743, 1.283725568143387, 1.270599239197784, 1.252502469911047, 1.226562832680814, 1.188108386583151, 1.130851180737285, 1.059155435155202, 0.9544645290479425, 0.7969866231157771, 0.5454418197581873, 0.1805192653504971, 0.06501198088671378, 0.04847157641350078, 0.06464207659082646, 0.5514364831487653, 0.9780931264241173, 1.159053472681637, 1.235964257876728, 1.26902087279772, 1.283544451331006, 1.290130663001437, 1.293226844112728, 1.294706863012109, 1.295332465864486, 1.294252294619113, 1.288864939616958, 1.279679250722385, 1.266320318041117, 1.247212317256791, 1.219310741363537, 1.177548074589396, 1.11661761299719, 1.038702993292247, 0.9241323327343359, 0.7500107590858497, 0.4654189412676132, 0.1271873185624313, 0.05816857111546718, 0.04889380401302876, 0.100250749168419, 0.729634575489462, 1.051963393123258, 1.188581907041767, 1.246732352121243, 1.271843799365567, 1.28300141849623, 1.288163096025218, 1.290652056425952, 1.291848127634666, 1.292134651466217, 1.288452588656543, 1.280129209268047, 1.267294435907646, 1.248673758590469, 1.221427054880761, 1.180666003033831, 1.120271317969751, 1.043892909914756, 0.9317593088977393, 0.7616769386686287, 0.4846171952530301, 0.1364135845777507, 0.05930437550257509, 0.0487773183403839, 0.09253451003180128, 0.7078791038125228, 1.042271702991805, 1.183965296804333, 1.244215191245004, 1.270185085367941, 1.281706797470767, 1.287038938647142, 1.289622019173436, 1.290878907564808, 1.291243439556013, 1.287651012382279]
		}

		for key, values in list(reference_data.items()):
			for i, t_data in enumerate(values):
				self.assertAlmostEqual(t_data, y[key][i], delta=(Settings.defaultTestAbsTol+t_data*Settings.defaultTestRelTol))




	def testMultipleSimulations(self):

		reference_data = [
			[0.0, 1.897738187453314, 3.756955433409792, 5.562177924708521, 7.287504219961273, 8.886453435701496, 10.27109268766486, 11.28772309320835, 11.80437071324164, 11.95991226988507, 11.99256438900284, 11.99865019516933, 11.9997559549625, 11.99995590896604, 11.99999203526398, 11.99999856126113, 11.99999974010935, 11.99999995305381, 11.99999999151893, 11.99999999846709, 11.99999999972277],
			[0.0, 0.9529744194118446, 1.897738143676265, 2.832956654063632, 3.756955345989689, 4.667608311587844, 5.56217777885444, 6.437073684702753, 7.287503869268203, 8.106957079719248, 8.886453073742068, 9.61352430912662, 10.27109490480332, 10.83711804675762, 11.28772610799255, 11.60760606676843, 11.80437164419517, 11.90945898048873, 11.95991216237439, 11.98264521841832, 11.99256436565644],
			[0.0, 0.3821004526202812, 0.7629982903165704, 1.142622670887443, 1.52089686811434, 1.897738084644651, 2.273055914286705, 2.646751099026785, 3.018714606196221, 3.388826562261258, 3.756955227031824, 4.122955353116793, 4.486666261422812, 4.847909671623483, 5.206487120386615, 5.562177583552335, 5.914733552284695, 6.263877332911981, 6.609296452309311, 6.950638286493137, 7.287503417781937],
			[0.0, 0.1911963667415279, 0.3821004525224335, 0.5727039601583825, 0.7629982906072463, 0.9529744123805983, 1.142622662304958, 1.331933761012865, 1.5208968421586, 1.709501935639981, 1.897738039117748, 2.085593198875023, 2.273055848907611, 2.460112780117928, 2.646751015818025, 2.83295646239224, 3.018714517584231, 3.204009916570333, 3.38882647127978, 3.573147542835388, 3.756955134446779]
		]

		m1 = self.__buildMichaelisModel()
		m2 = self.__buildMichaelisModel()
		m2.listOfSpecies.getBySbmlId("E").setValue(5)
		m3 = self.__buildMichaelisModel()
		m3.listOfSpecies.getBySbmlId("E").setValue(2)
		m4 = self.__buildMichaelisModel()
		m4.listOfSpecies.getBySbmlId("E").setValue(1)

		sim = TimeseriesSimulation([m1, m2, m3, m4], time_min=0, time_ech=1, time_max=20, keep_files=True)
		sim.run()

		for i, (_, y) in enumerate(sim.getRawData()):
			for j, t_data in enumerate(y['P']):
				self.assertAlmostEqual(t_data, reference_data[i][j], delta=1e-4)

