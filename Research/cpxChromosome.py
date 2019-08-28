#cpxChromosome.py
#Game
#Abraham Oliver and Jadan Ercoli

import random

from move import Move

from GamePieces.pathCount import PathCounter
from baseChromosome import Chromosome as Base


class Chromosome (Base):
	"""Child class specified for the complex learning chromosome"""
	isChromosome = True
	def __init__(self, data = []):
		self.range = 7
		#Longest path of player
		self.cPath = PathCounter([])
		#Longest path of opponent
		self.oPath = PathCounter([])
		super(Chromosome, self).__init__(data)

	def str(self):
		return "CPX CHROMOSOME with DATA = " + str(self.data)

	def __str__(self):
		return "CPX"

	def randomData(self):
		"""Creates data set of 5 values between 1 and 'self.range'(5)
		for the 6 weights of the reward function parameters"""
		d = []
		for i in range(6):
			d.append(random.choice(range(1,self.range)))
		self.data = d

	def play(self, brd, GUI = 0):
		final = 0
		while final == 0 or type(final) != Move:
			#Record, print, and play final move
			final = self.bestMove(brd, GUI)
		self.recordMove(final)
		brd.playMove(final)
		return final

	def bestMove(self, brd, GUI = 0):
		#Create copy of board to prevent accidental movement of pieces
		board = brd.copyBoard()
		#Find original longest paths to save time when testing moves
		self.cPath = PathCounter(brd)
		self.cPath.findLongestColor(self.color)
		#Find original path for opponent
		self.oPath = PathCounter(brd)
		if self.color == 1: self.oPath.findLongestColor(2)
		elif self.color == 2: self.oPath.findLongestColor(1)

		#Find all available
		avail = board.findAvail()

		#NORMAL MOVES
		#Make Stack of best moves, starting with the first two
		# moves with the worst fitness
		bestNormal = Pool(Move(avail[0], avail[1], -100))

		#For every two pieces, of opposite colors, with the
		# first being of the player
		#print "START NORMAL MOVES"
		for i in avail:
			if GUI != 0: GUI.update(brd)
            #Is this piece its color?
			if i.color !=  self.color: continue

			for j in avail:
				#Is this piece opponent?
				if j.color == self.color: continue
				#Create move with these pieces
				x = Move(i, j)
				#Set the fitness to the reward of the move
				x.setFitness(self.reward(x, board))
				#If best move, make new pool of new fitness
				if x.fitness > bestNormal.fitness:
					bestNormal = Pool(x)
				#If same as other highests, add to pool
				elif x.fitness == bestNormal.fitness: bestNormal.add(x)

		#SOLID MOVES
		#print "START SOLID MOVES"
		bestSolid = Pool(Move(avail[0], avail[1], -100))
		#Find two personal pieces
		pp = 0
		for i in avail:
			if i.color == self.color and pp == 0:
				pp = i
				break
		#Find an opponent piece
		op = 0
		for i in avail:
			if i.color != self.color and op == 0:
				op = i
				break

		#Analyze solid moves
		for i in avail:
			if GUI != 0: GUI.update(board)
			#Is this piece its color/ If not: next
			if i.color != self.color: continue
			#Create move
			x = Move(op, i)
			#Set fitness
			x.setFitness(self.solidReward(x, board))
			#Set to solidify
			x.m1 = pp
			#If best move, make new pool of new fitness
			if x.fitness > bestSolid.fitness:
				bestSolid = Pool(x)
			#If same as other highests, add to pool
			elif x.fitness == bestSolid.fitness: bestSolid.add(x)

		#Select the best move
		bestN = bestNormal.choose()
		bestS = bestSolid.choose()
		bN = bestN.fitness * self.data[4] * self.data[0]
		#print "BN " + str(bN)
		bS = bestS.fitness * self.data[5] * self.data[1]
		#print "BS " + str(bS)

		if bN >= bS: best = bestN
		else: best = bestS

		#Translate coordinates
		final = brd.translate(best, board)
		return final

	def reward(self, move, board):
		"""Returns numerical value of how effective a
		move will be in the game. Uses values defined
		by the machine learning to weight diferent variables

		NOTE : includeImped should be true when called first time
		but she be false when called in a function within reward
		such as future imped

		DATA:
		0 -- Constructive
		1 -- Destructive
		2 -- Added to personal Chain (1 because === constructive)
		3 -- Added to opponent's Chain (hopefully negative)
		4 -- Works for improvement (opposite of impediment)
		5 -- Impedes opponent's next move
		"""
		data = self.data

		#Constructives
		#Number added to personal chain (PA = Personal Added)
		PA = self.CLA(move, board, personal = True)
		C = data[0] * (data[1] * PA)

		#Destructives
		#Added to opponent's (negative = good for player) (OA = Opponent Added)
		OA = -self.CLA(move, board, personal = False)
		D = data[1] * (data[2] * OA)

		return C + D

	def solidReward(self, move, board):
		"""
		BASICALLY SWITCHES TO OPPONENT

		DATA:
		0 -- Constructive
		1 -- Destructive
		2 -- Added to personal Chain
		3 -- Added to opponent's Chain (hopefully negative)
		4 -- Impedes opponent's next move
		5 -- Works for improvement (opposite of impediment)
		"""
		data = self.data

		#Make sure doesnt hurt self
		if self.CLA(move, board, personal = True) < 0: return 0

		#Constructives
		#Number added to personal chain (PA = Personal Added)
		PA = self.CLA(move, board, personal = False)
		#print "PA = " + str(PA)
		C = data[0] * (data[1] * PA)
		#print "C = " + str(C)

		#Destructives
		#Added to opponent's (negative = good for player) (OA = Opponent Added)
		OA = -self.CLA(move, board, personal = True)
		#print "OA = " + str(OA)
		D = data[1] * (data[2] * OA)
		#print "D = " + str(D)
		#print "C+D = " + str(C+D) + "\n"
		return C + D

class Pool:
	def __init__(self,m):
		self.moves = [m]
		self.fitness = m.fitness
	def add(self, m):
		self.moves.append(m)
	def choose(self):
		#Choose a random move from the equal moves
		return random.choice(self.moves)