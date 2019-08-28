#gTournament.py
#Game
#Abraham Oliver and Jadan Ercoli

import random
import time

from Research.analysis import Storage

from basePopulation import Population as Pop
from game import Game


class Tournament (object):
	def __init__(self, size, path, _type1, _type2 = None):
		self.size = size
		self.path = path
		self.storage = Storage(path)
		self.storage.save()
		self._type1 = _type1
		self._type2 = _type2
		#Create first population
		self.pops = 1
		self.pop1 = Pop(size, _type1)
		if _type1 != _type2 and _type2 != None:
			#If two different kinds, make second
			self.pops = 2
			self.pop2 = Pop(size, _type2)
		
	def play(self, minRuns):
		self.savePopulations()
		#TODO Killer
		while True:
			"""Plays a minimum of 'minruns' games
				per member per generation"""
			time0 = time.clock()
			for i in range(minRuns):
				#Create list of possible players
				if self.pops == 1:
					chromos = []
					opp = []
					chromos += self.pop1.members
					#Shuffle list
					random.shuffle(chromos)
					#Pair off
					while len(chromos) >= 2:
						opp.append([chromos.pop(), chromos.pop()])
				elif self.pops == 2:
					m1 = []
					m2 = []
					opp = []
					#Create shuffleable lists
					m1 += self.pop1.members
					m2 += self.pop2.members
					#Shuffle
					random.shuffle(m1)
					random.shuffle(m2)
					#Pair Off
					while len(m1) >= 1 and len(m2):
						opp.append([m1.pop(), m2.pop()])
				#Play Games
				for p1, p2 in opp:
					#Play game (play again if tie)
					tie = True
					numTies = 0
					g = 0
					while tie:
						g = Game(p1, p2)
						g.play()
						tie = g.tie
						self.storage.record(g.record)
						#Break if color bug occurs
						if numTies > 2: break
				#Save the population
				self.savePopulations()
			print "+++++++++++++++++++++++++++++++++++"
			print "+++++++++++++++++++++++++++++++++++"
			self.savePopulations()
			self.pop1.endGeneration()
			if self.pops == 2:
				self.pop2.endGeneration()
			self.savePopulations()
			print "POPULATION TIME : ", (time.clock() - time0)
			print "%s'S RECORD : %s" % (str(self.pop1), str(self.pop1.record))
			if self.pops == 2:
					print "%s'S RECORD : %s" % (str(self.pop2), str(self.pop2.record))
			print "+++++++++++++++++++++++++++++++++++"
			print "+++++++++++++++++++++++++++++++++++"

	def savePopulations(self):
		if self.pops == 2:
			name1 = self.path + "A"
			self.pop1.savePop(name1)
			name2 = self.path + "B"
			self.pop2.savePop(name2)
		else:
			name = self.path + "POP"
			self.pop1.savePop(name)
