#gBoard.py
#Game
#Abraham Oliver and Jadan Ercoli

#Imports
from Permaximize.GamePieces.move import Move
import Permaximize.GamePieces.piece as piece

#Main class for Board
class Board:
	#Set up instance
	def __init__(self):
		self.board = []
		self.newBoard()

	def __len__(self):
		"""Allows for use of 'len'"""
		return len(self.board)

	def __getitem__(self, key):
		"""Allows for indexing"""
		return self.board[key]

	def __iter__ (self):
		"""Allows for iteration"""
		for i in self.board: yield i

	def __contains__(self, item):
		"""Allows for use of 'in' operator"""
		if item in self.board: return True
		else: return False

	def copyBoard(self):
		"""Returns a new board object with same data as current"""
		b = Board()
		b.newBoard(self.board)
		return b

	def newBoard(self, brd = []):
		"""Creates new board and sets to 'self.board'"""
		if brd == []:
			#Completely new board
			#Create list of 32 pieces of one color and 32 of the other
			b = []
			for i in range(8):
				for j in range(4):
					if i % 2 == 0:
						b.append(piece.Piece(1))
						b.append(piece.Piece(2))
					else:
						b.append(piece.Piece(2))
						b.append(piece.Piece(1))
		elif brd[0].__class__ == piece.Piece:
			#If board made of piece data
			b = []
			for i in brd:
				b.append(i.copy())
		else:
			#If board made of color data
			b =[]
			for i in brd:
				b.append(piece.Piece(i))

		#Initialize
		#Shuffling is not supported at this time
		#random.shuffle(b)
		self.board = b

	def findAvail(self):
		"""Return list of all unused pieces"""
		a = []
		for i in self.board:
			if not i.state:
				a.append(i)
		return a

	def playMove(self, move):
		"""Plays the move on the board"""
		#Find pieces on board
		p1 = self.find(move.m1)
		p2 = self.find(move.m2)
		move.locate(p1,p2)
		#If either is permentized, quit
		if self.board[p1].state or self.board[p2].state:
			return False
		#Switch pieces
		temp = self.board[p1]
		self.board[p1] = self.board[p2]
		self.board[p2] = temp
		#Permentizes
		self.board[p2].perm()
		return True

	def find(self, p):
		"""Locate by 'piece' and return location"""
		#Throw error if not a piece
		if p.__class__ != piece.Piece:
			return None
		#Otherwise, find the piece
		for i in range(len(self.board)):
			if self.board[i] == p:
				return i

	def translate(self, move, board):
		"""Translate a move from board to a move on self.board"""
		m1 = self.board[board.find(move.m1)]
		m2 = self.board[board.find(move.m2)]
		return Move(m1, m2)

	#Print board to console (for debug only)
	def printBoard(self, mode = 0):
		"""Prints poard to the CLI
		Mode = 0 -- print colors
		Mode = 1 -- print ids
		Mode = 2 -- fancy board"""
		if mode == 0 or mode == 1:
			for i in range(8):
				toPrint = ""
				for j in range(8):
					if mode == 0:
						toPrint += str(self.board[(8 * i) + j].color)
						toPrint += " "
					else:
						toPrint += str(self.board[(8 * i) + j].id)
						toPrint += " "
						if self.board[(8 * i) + j].id < 10: toPrint += " "
				print(toPrint)
		elif mode == 2:
			print("\n+----+----+----+----+----+----+----+----+")
			for i in range(8):
				toPrint = "|"
				toPrint2 = "|"
				for j in range(8):
					p = self.board[(8 * i) + j]
					#Create first row of pieces
					if p.color == 1:
						if p.state: toPrint += " Ol |"
						else: toPrint += " OO |"
					elif p.color == 2:
						if p.state: toPrint += " -+ |"
						else: toPrint += " -- |"

					#Create label row
					loc = str(self.find(p))
					if int(loc) < 10: loc = " %s" % (loc)
					toPrint2 += " %s |" % (loc)
				print(toPrint)
				print(toPrint2)
				print("+----+----+----+----+----+----+----+----+")
