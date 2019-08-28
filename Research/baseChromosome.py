#baseChromosome.py
#Game
#Abraham Oliver and Jadan Ercoli

import random
from copy import deepcopy

from Research.matingHistory import History

from AI import ai


class Chromosome (ai.AI):
	"""Base class for chromosome of a population"""
	def __init__(self, data = []):
		self.data = data
		self.fitness = 0
		self.mutationRate = .05
		self.mateProb = .1
		self.gen = 1
		if not data:
			self.randomData()
		else:
			self.data = data
		self.track = True
		if self.track:
			self.history = History(self.data)
		self.avg = False
		super(Chromosome, self).__init__()

	def randomData(self): self.data = [] #Overrided in all children

	def randomInt(self, start, stop):
		"""Returns a random integer between start and stop inclusive"""
		return random.randint(start, stop)

	def mutate(self):
		"""Mutates a random value"""
		m = random.random()
		#If in the mutation rate
		if m < self.mutationRate:
			r1, r2 = 0, 0
			while r1 == r2:
				r1 = random.randint(0,len(self.data) - 1)
				r2 = random.randint(0,len(self.data) - 1)
			temp = self.data[r1]
			self.data[r1] = self.data[r2]
			self.data[r2] = temp

	def mate(self, partner):
		"""Swaps the front and back parts of the data at a random
			point (not endpoints) between two chromosomes"""
		data = self.data
		#Save data pre-mate
		if self.track:
			self.history.preMate(partner)
			partner.history.preMate(self)
		#Find random split point
		split = random.randrange(1,len(data)- 1)
		#Split datas
		front1 = data[:split]
		back1 = data[split:]
		front2 = partner.data[:split]
		back2 = partner.data[split:]
		#Concencrate into new data
		newData1 = front1 + back2
		newData2 = front2 + back1
		partner.data = newData2
		self.data = newData1
		if self.track:
			self.history.postMate(self)
			partner.history.postMate(partner)

	def convertData(self):
		"""Overridden in children who need it"""
		return self.data

	def calcFitness(self):
		"""Calculates average win ratio"""
		#Protect for divide by zero
		if len(self.scoreRecord) > 0:
			total = 0
			for s in self.scoreRecord:
				total += s
			self.fitness = (total / len(self.scoreRecord)) + 30
			return self.fitness
		else:
			if self.avg:
				return self.fitness
			else:
				self.fitness = 1
				return 1

	def copy(self):
		"""Returns a new choromosome with the same members"""
		return deepcopy(self)