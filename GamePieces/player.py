#player.py
#Game
#Abraham Oliver and Jadan Ercoli

from Permaximize.GamePieces.move import Move

class Player (object):
	isChromosome = False
	def __init__(self):
		self.color = 0
		self.record = [0,0]
	
	def __str__(self):
		return "PLY"

	def setColor(self,color):
		self.color = color

	def win(self):
		self.record[0] += 1

	def lose(self):
		self.record[1] += 1
	
	def play(self, board, gui):
		breaker = False
		while not breaker:
			breaker = gui.update(board, player = True)
