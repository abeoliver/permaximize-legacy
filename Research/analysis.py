#recorder.py
#Game
#Abraham Oliver and Jadan Ercoli

import pickle

from board import Board
from plexQueue import Queue

from GamePieces.pathCount import PathCounter as PC


class Record (object):
	def __init__(self, board):
		self.board = board
		self.queue = Queue()

	def __len__(self):
		return len(self.queue)

	def __getitem__(self, i):
		return self.queue[i]

	def __iter__(self):
		for i in self.queue:
			yield i
	
	def recordMove(self, move):
		self.queue.enqueue(move)
		
class Replay (object):
	def __init__(self, record):
		self.record = record
		self.board = self.replayAll()
		self.finals = self.finalPaths()
		self.score = (len(self.finals[0]), len(self.finals[1]))

	def replayAll(self):
		"""Same as 'replay' for all recorded moves"""
		return self.replay(len(self.record))

	def replay(self, until):
		"""Returns board of game only finished to 'until'"""
		b = Board()
		for i in range(until):
			move = b.translate(self.record[i], self.record.board)
			b.playMove(move)
		return b

	def finalPaths(self, board = None):
		if board == None:
			counter = PC(self.board)
		else:
			counter = PC(board)
		longest = counter.findLongest()
		if longest.color == 1:
			return (longest, counter.findLongestColor(2))
		elif longest.color == 2:
			return (counter.findLongestColor(1), longest)

	def calcScore(self, until):
		"""Returns score of game at point 'until'"""
		rep = self.replay(until)
		finals = self.finalPaths(rep)
		return (len(finals[0]), len(finals[1]))

class Storage (object):
	def __init__(self, filePath):
		self.path = filePath
		self.games = []

	def __iter__(self):
		for i in self.games:
			yield i

	def __getitem__(self, index):
		return self.games[index]

	def __len__(self):
		return len(self.games)

	def record(self, record, save = True):
		"""Records game to 'self.game'. If 'save', save to file"""
		self.games.append(record)
		if save:
			self.save()

	def save(self):
		fileName = self.path + "GameRecords.stor"
		f = open(fileName, "w")
		pickle.dump(self, f)
		f.close()

	def load(self):
		fileName = self.path + "GameRecords.stor"
		f = open(fileName, "r")
		ret = pickle.load(f)
		f.close()
		return ret