#aiDesigned.py
#Game
#Abraham Oliver and Jadan Ercoli

from AI.cpxChromosome import Chromosome as CPX

from permaximize.GamePieces.pathCount import PathCounter


class Player (CPX):
	isChromosome = False
	def __init__(self, strategy = [1,1,1,1,1,1]):
		self.cPath = PathCounter([])
		self.oPath = PathCounter([])
		self.strategy = strategy
		super(Player, self).__init__(strategy)
	
	def __str__(self):
		return "AID"

	def str(self):
		return "AID"