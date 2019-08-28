#basePopulation.py
#Game
#Abraham Oliver and Jadan Ercoli

try:
	import cPickle as pkl
except:
	import pickle as pkl
from random import random, choice

class Population (object):
	"""Base class for population, a mass of chromosomes

		Attributes:
			size -- number of members in population
			gen -- current generation number
			fitness -- fitness of population
			_type -- CLASSOBJ of members
			members -- list of members
	"""
	def __init__(self, size, _type, members = []):
		"""Size = size of pop, _type = CLASS OBJECT"""
		self.size = size
		self.record = [0,0]
		self.scoreRecord = []
		self.gen = 1
		self.fitness = 0
		self.name = "GameRecords\\Abe\\A"
		self._type = _type #ClassType
		#If empty population, create a random one
		if not members: self.randomPop(size)
		else: self.members = members
		self.best = self.members[0]

	def __iter__(self):
		"""Allows for iteration"""
		for i in self.members:
			yield i

	def __len__(self):
                return len(self.members)

	def __str__(self):
		return str(self.members[0]) + " Pop Gen #" + str(self.gen)

	def __getitem__(self, index):
		"""Allows for indexing and slicing"""
		return self.members[index]

	def debugBest(self, compared = None):
		print "DEBUG BEST CHROMOSOME"
		print "BEST DATA -- %s || Fit -- %i" % \
			  (str(self.best.data), self.best.calcFitness())
		if compared:
			print "COMP DATA -- %s || Fit -- %i" % \
			  (str(compared.data), compared.calcFitness())
		print ""

	def savePop(self, name = ""):
		"""Save population to file 'name' or 'self.name' w/ pickle to the path set in globalVariables.py"""
		#Save population
		if name == "": name = self.name
		else: self.name = name
		fileName = "%s%i" % (name, self.gen)
		f = open(fileName, "w+")
		pkl.dump(self, f)
		f.close()

	def loadPop(self, name = ""):
		"""Load population from file 'name' or 'self.name' w/ pickle from the path set in globalVariables.py"""
		#If not a chromosome, end
		if not self._type.isChromosome:
			return Population(1, self._type)
		if self.name == "": name = self.name
		f = open(name, "r")
		ret = pkl.load(f)
		f.close()
		return ret

	def randomPop(self, size):
		"""Creates random population of size 'size' of of initiated type"""
		m = []
		for i in range(size):
			m.append(self.new())
		self.members = m

	def take(self, size, data):
		"""If size is positive, return top 'size' best fitnessed,
		if negative, return bottom worst"""
		d = []
		for i in data:
			i.calcFitness()
			d.append(i)
		#NOTE : sorted from least to most naturally
		if size <= 0: d = sorted(d, key = lambda x: x.fitness)
		elif size > 0: d = sorted(d, key = lambda x: x.fitness, reverse = True)
		return d[-1 * abs(size):]

	def finalizeRecord(self):
		wins = 0
		loss = 0
		for i in self.members:
			wins += i.record[0]
			loss += i.record[1]
		self.record = [wins, loss]
		self.finalizeFitness()

	def finalizeFitness(self):
		#Take average fitness of top half of chromosomes
		avg = 0
		for i in range(len(self.members) / 2):
			avg += self.members[i].calcFitness()
		self.fitness = avg / (len(self.members) / 2.0)

	def createMateProbs(self, members):
		m = members
		#Calculate fitnesses of all members
		mateProbTotal = 0
		for i in m:
			if not i.avg:
				i.calcFitness()
				i.mateProb = 0
				mateProbTotal += i.fitness
		#For avgs
		for i in m:
			if i.avg:
				fit = min(m, key = lambda x: x.fitness).fitness
				i.fitness = fit
				i.mateProb = 0
				mateProbTotal += i.fitness

		#Assign mateProd
		mateBase = 1 / float(mateProbTotal)
		#Assign mateProb
		for i in m:
			i.mateProb = i.fitness * mateBase

	def pickMates(self, members):
		m = members
		#Create list of representation based on mateProb
		selection = []
		for i in m:
			#Number of representatives
			p = int(i.mateProb * 100)
			#Add number of reps to overall selection
			for j in range(p):
				selection.append(i)
		#Pick two different mates
		mate1 = choice(selection)
		mate2 = choice(selection)
		while mate1 == mate2:
			mate2 = choice(selection)
		return [mate1, mate2]

	def endGeneration(self):
		"""End a generation of the population. Mate, mutate, kill, etc."""
		#Save current
		self.savePop()
		self.finalizeRecord()

		#If not a chromosome, end
		if not self._type.isChromosome:
			self.gen += 1
			self.savePop()
			return 0

		#Get best and 2nd Best in final populations
		self.members = sorted(self.members, key = lambda x: x.fitness)
		self.best = self.members[0]
		best = [self.members[0].copy(), self.members[0].copy(),
				self.members[1].copy()]
		for i in best:
			i.clearRecord()

		#Create generation pools
		m = []
		m += self.members
		nextGen = best

		#Add two copies of chromosomes that are the average of the saved (the best)
		avg = []
		for i in range(len(m[0].data)):
			a = 0
			for k in m:	a += k.convertData()[i]
			#Append at correct data position an integer, rounded version of the average
			avg.append(int(round(float(a) / len(m))))
		new = self.new(data = avg)
		new.avg = True
		for i in range(2): m.append(new)

		#Add random
		for i in range(self.size / 10):
			n = self.new()
			n.fitness = min(m, key = lambda x: x.fitness).fitness
			m.append(n)

		self.createMateProbs(m)

		#Mate random selections from the members into nextGen until full
		while len(nextGen) < self.size:
			mates = self.pickMates(m)
			#Pop mates so not to be used again
			nm = []
			for i in range(len(m)):
				if m[i] not in nm:
					if m[i] != mates[0] and m[i] != mates[1]:
						nm.append(m[i])
			m = nm

			#Mate
			mates[0].mate(mates[1])

			for i in mates:
				i.clearRecord()
				nextGen.append(i)

		#Finish operations
		for i in nextGen:
			#Mutate
			if i != self.best:
			    i.mutate()
			i.mateProb = 0

		#Finalize
		self.members = nextGen
		self.gen += 1
		self.savePop()

	def new(self, data = []):
		return self._type(data)