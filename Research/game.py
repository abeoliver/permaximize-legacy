#gGame.py
#Game
#Abraham Oliver and Jadan Ercoli

#Imports
import time

from Research.analysis import Record

from GamePieces.pathCount import PathCounter


class Game:
	def __init__(self, p1, p2):
		#Create new board
		self.createNew()
		#Start Game
		#TODO Change back to 10
		self.allowed = 10
		self.record = Record(self.board)
		self.tie = False
		self.p1 = p1
		self.p2 = p2

	def createNew(self):
		self.board = board.Board()

	def playTurn(self, p1, p2):
		"""Give both players their turns"""
		move1 = p1.play(self.board)
		self.board.playMove(move1)
		self.record.recordMove(move1)
		move2 = p2.play(self.board)
		self.board.playMove(move2)
		self.record.recordMove(move2)
		print("."),

	def play(self):
		#Start timer
		time0 = time.clock()
		print "GAME IN PROGRESS",
		#Set colors
		self.p1.setColor(1)
		self.p2.setColor(2)
		#Make sure colors were set
		if self.p1.color == self.p2.color:
			self.tie = True
			return 0
		for i in range(self.allowed):
			self.playTurn(self.p1,self.p2)
		#Check winner, if tie, play until winner
		overtimeCount = 0
		while True:
			#Check Winner
			pc = PathCounter(self.board)
			longest = pc.findLongest()
			winColor = longest.color
			#Check loser
			if winColor == self.p1.color:
				loseLongest = pc.findLongestColor(self.p2.color)
			elif winColor == self.p2.color:
				loseLongest = pc.findLongestColor(self.p1.color)
			else:
				print "\nATTENTION NEEDED"
				print "DEBUG ::: WIN-%i of %s" % (winColor, str((self.p1.color, self.p2.color)))
				print "DEBUG ::: %s" % (str((len(longest), len(loseLongest))))
				break
			#Break if not tie
			if len(longest) == len(loseLongest):
				#If there have been more than 5 overtime moves
				if overtimeCount >= 5:
					#No wins, no losses, a tie
					print "\n========================================="
					print "TIE: NO WINS NO LOSSES -- %i vs %i" % (
						len(longest), len(loseLongest))
					print "DEBUG :: COLORS (%i, %i, WIN %i) LENS (%i, %i)" % (
						self.p1.color, self.p2.color, winColor,
						len(pc.findLongestColor(self.p1.color)),
						len(pc.findLongestColor(self.p2.color)))
					print "=========================================\n"
					self.tie = True
					self.p1.finalize(0)
					self.p2.finalize(0)
					return 0
				else:
					self.playTurn(self.p1,self.p2)
					overtimeCount += 1
			else:
				break
		#End timer
		finalTime = time.clock() - time0
		#Finalize winners, change records
		if winColor == self.p1.color:
			winner = self.p1
			loser = self.p2
			self.p1.finalize(len(longest) - len(loseLongest))
			self.p2.finalize(len(loseLongest) - len(longest))
		else:
			winner = self.p2
			loser = self.p1
			self.p2.finalize(len(longest) - len(loseLongest))
			self.p1.finalize(len(loseLongest) - len(longest))
		
		#Print Game information after play is completed
		print "\n========================================="
		print "Game Brief"
		print "Time    : %s seconds" % (str(finalTime))
		print "Winner  : %s (%s)" % (winner.str(), str(winner.gen))
		print "Loser   : %s (%s)" % (loser.str(), str(loser.gen))
		print "Score   : %i - %i" % (len(longest), len(loseLongest))
		print "Records : W%s vs. L%s" % (str(winner.record), str(loser.record))
		#self.board.printBoard(2)
		print "========================================="

		#Try cleaning up
		del pc, winner, loser, winColor, longest, loseLongest
