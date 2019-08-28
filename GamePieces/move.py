#move.py
#Game
#Abraham Oliver and Jadan Ercoli

class Move (object):
	"""Contains information like fitness of a move and the pieces moved"""
	def __init__(self, m1, m2, fitness = 0):
		"""m1 and m2 are Piece objects"""	
		self.m1 = m1
		self.m2 = m2
		self.move = (m1,m2)
		self.fitness = fitness
		self.loc = (0,0)

	def __str__(self):
		return "(%s, %s) F=%s" % (str(self.m1), str(self.m2), str(self.fitness))
		
	def setFitness(self, fitness):
		self.fitness = fitness

	def locate(self, loc1, loc2):
		self.loc = (loc1, loc2)
		self.m1.setName(str(loc1))
		self.m2.setName(str(loc2))
		self.name = str(loc1) + "-" + str(loc2)
