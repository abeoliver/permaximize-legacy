#AI.py
#Game
#Abraham Oliver and Jadan Ercoli

from Permaximize.GamePieces.move import Move

from Permaximize.GamePieces.pathCount import PathCounter


class AI(object):
	"""Abstract class that handles every type of AI"""
	def __init__(self):
		self.record = [0,0]
		self.longRecord = []
		self.scoreRecord = []
		self.gen = 1
		self.color = 0
		self.lastMove = Move(0,0)
		self.lastScore = 0
		self.avg = False
	
	def __str__(self):
		return "AI"

	def str(self):
		return "AI"

	def setColor(self, color):
		self.color = color

	def clearRecord(self):
		self.record = [0,0]
		self.longRecord = []
		self.scoreRecord = []

	def printRecord(self):
		print("RECORD : %s" % str(self.record))
		r = ""
		for i in self.longRecord:
			r += str(i)
		print("LONG : %s" % r)
	
	def play(self, board):
		"""Takes 'board' and returns a Move object"""
		return Move(board.board[0], board.board[0])
	
	def recordMove(self, move):
		self.lastMove = move
	
	def printMove(self, board):
		lm = self.lastMove
		print("AI MOVES (%s, %s)" % (str(board.find(lm.m1)), str(board.find(lm.m2))))
	
	def finalize(self, scoreDif):
		"""Change records, finalized fitnesses"""
		if scoreDif > 0: 
			self.record[0] += 1
			self.longRecord.append(1)
		elif scoreDif < 0:
			self.record[1] += 1
			self.longRecord.append(0)
		self.scoreRecord.append(scoreDif)
		self.lastScore = scoreDif

	def binaryRecord(self, mode = 1):
		r = []
		for i in self.scoreRecord:
			if i > 0: r.append(1)
			elif i < 0: r.append(0)
			else: r.append(8)
		if mode == 1:
			return r
		elif mode == 2:
			s = ""
			for i in r: s += str(i)
			return s

	def averageScore(self):
		a = 0
		for i in self.scoreRecord: a += i
		return float(a) / len(self.scoreRecord)

	def CLA(self, move, board, personal = True):
		"""Calculates the length added to a chain from 'move' on 'board'. Done for 'self.color'. "Added-Length-Positive"""
		cpy = board.copyBoard()
		#Translate coordinates
		cpyMove = cpy.translate(move, board)
		#Find longest chain
		if personal:
			color = self.color
			p0 = self.cPath
		else:
			if self.color == 1: color = 2
			elif self.color == 2: color = 1
			p0 = self.oPath
		#Make move and check difference
		cpy.playMove(cpyMove)
		p1 = PathCounter(cpy)
		p1.findLongestColor(color)
		return len(p1.longPath) - len(p0.longPath)
