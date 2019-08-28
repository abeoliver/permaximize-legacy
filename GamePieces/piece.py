#gPiece.py
#Game
#Abraham Oliver and Jadan Ercoli

class Piece:
	def __init__(self, color):
		self.color = color
		self.state = False
		self.selected = False

	def setName(self, name):
		self.name = str(name)

	def perm(self):
		"""Permentize piece"""
		self.state = True
	
	def copy(self):
		"""Returns a cloned piece"""
		p = Piece(self.color)
		p.state = self.state
		return p
