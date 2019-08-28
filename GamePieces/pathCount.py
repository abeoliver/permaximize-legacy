#gPathCount.py
#Game
#Abraham Oliver and Jadan Ercoli

import Permaximize.GamePieces.board as Board

class Path:
	"""Represents a path with path and length"""
	def __init__(self,path):
		self.path = path
		if path != []: self.color = path[0].color

	def __len__(self):
		"""Allow for use of length"""
		return len(self.path)

	def __str__(self):
		"""Allows for type casting to string"""
		printer = ""
		for i in self.path:
			printer += str(i.color)
		return printer

	def __getitem__(self, key):
		"""Allow for indexing"""
		return self.path[key]

	def __iter__(self):
		"""Allow for iteration"""
		for i in self.path: yield i

	def __cotains__(self, item):
		"""Allow for use of 'in' operator"""
		if item in self.path: return True

class PathCounter:
	"""Takes a board and finds/counts the paths"""
	def __init__(self, board):
		self.b = board
		N, S, W, E = -8, 8, -1, 1
		self.dirs = [N, S, W, E]
		self.longPath = Path([])

	def findPath(self, start):
		"""Find path and then translate into a path object"""
		full = [start]
		path = self._findPath(full)
		#Delete Duplicates
		interm = []
		for i in path:
			if i not in interm: interm.append(i)
		#Translate back into 'Piece' objects
		final = []
		for i in interm:
			final.append(self.b.board[i])
		#See if it is the longest
		if len(final) > len(self.longPath):
			#Set longest to current
			self.longPath = Path(final)
		return Path(final)

	def _findPath(self, path):
		"""Find the path from 'path' last point"""
		#Start a path with 'start' as the first piece
		possibles = []
		start = path[len(path) - 1]
		#Go through each direction
		for i in self.dirs:
			new = start + i
			#Eliminate if used
			if new in path: continue
			#Eliminate if impossible
			elif new < 0 or new >= 64: continue
			#Eliminate if off left side
			elif (start % 8) == 0 and i == -1: continue
			#Eliminate if off right side
			elif ((start + 1) % 8) == 0 and i == 1: continue
			#If colors match, add to possibles
			elif self.b.board[new].color == self.b.board[start].color:
				possibles.append(i)
		if possibles == []: return path #If no more possibles, go back in recursion
		for i in possibles:
			#For each possible, advance that direction
			#Append the new start piece to the path
			path.append(start + i)
			#Go through again recursively
			path = self._findPath(path)
		#Return final path
		return path

	def findLongest(self):
		"""Saved in case needed again"""
		used = []
		for i in self.b.board:
			if i not in used:
				p = self.findPath(self.b.board.index(i))
				for j in p.path: used.append(j)
		return self.longPath

	def findLongestTrial(self):
		used = []
		for i in self.b.board:
			if i not in used:
				#Create a process
				p = process.Process(self.findPath)
				#Run function
				a = p.run(self.b.board.index(i))
				for j in a.path: used.append(j)
		return self.longPath


	def findLongestColor(self, color):
		used = []
		longest = Path([])
		for i in self.b:
			if (i not in used) and (color == 1 or color == 2):
				if i.color == color:
					p = self.findPath(self.b.find(i))
					if len(longest) < len(p):
						longest = p
					for j in p.path: used.append(j)
		return longest

#Main
"""b = Board.Board()
data = [1, 2, 2, 2, 1, 2, 1, 2,
	1, 1, 1, 2, 2, 1, 2, 1,
	1, 2, 1, 2, 1, 2, 1, 2,
	2, 1, 2, 1, 2, 1, 2, 1,
	1, 2, 1, 2, 1, 2, 1, 2,
	2, 1, 2, 1, 2, 1, 2, 1,
	1, 2, 1, 2, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1]
b.newBoard(data)
p = PathCounter(b)
time0 = time.clock()
p.findLongest()
print "TIME : ", time.clock() - time0
time0 = time.clock()
p.findLongestTrial()
print "TIME : ", time.clock() - time0

orig = [1, 2, 1, 2, 1, 2, 1, 2,
	2, 1, 2, 1, 2, 1, 2, 1,
	1, 2, 1, 2, 1, 2, 1, 2,
	2, 1, 2, 1, 2, 1, 2, 1,
	1, 2, 1, 2, 1, 2, 1, 2,
	2, 1, 2, 1, 2, 1, 2, 1,
	1, 2, 1, 2, 1, 2, 1, 2,
	2, 1, 2, 1, 2, 1, 2, 1]"""
