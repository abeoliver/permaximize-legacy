#PlayPermaximize.py
#Game
#Abraham Oliver and Jadan Ercoli

from Permaximize.GamePieces.board import Board
from Permaximize.GamePieces.move import Move

from Permaximize.GUI.gameGUI import GUI
from Permaximize.GamePieces.pathCount import PathCounter as PC


class Game:
    def __init__(self, p1, p2, guiClass = GUI, width = 740, height = 740, circle = 37):
        # Initialize
        self.p1 = p1
        self.p2 = p2
        self.players = [self.p1, self.p2]
        self.GUI = guiClass(self, width = width, height = height, circle = circle)
        self.board = Board()
        self.winnerIndex = 0

        # Dynamic variables
        self.selected = []
        self.turns = 0
        self.tie = False

    def play(self, loop = False):
        # Less than 20 moves or a tie, play moves
        self.players[0].setColor(1)
        self.players[1].setColor(2)
        while self.turns < 20 or self.tie:
            self.GUI.update(self.board)
            # Play turns for each player
            for p in self.players:
                self.GUI.update(self.board)
                p.play(self.board, self.GUI)
                self.turns += 1

            # Check for winner
            pc = PC(self.board)
            longest = pc.findLongest()
            winColor = longest.color
            # Check loser
            if winColor == 1:
                loseColor = 2
                loseLongest = pc.findLongestColor(2)
            elif winColor == 2:
                loseColor = 1
                loseLongest = pc.findLongestColor(1)
            # Check if tie
            if longest == loseLongest:
                self.tie = True
            else:
                self.tie = False

        # Leave final
        if winColor == 1:
            self.GUI.winColor = self.GUI.blue
            self.winnerIndex = 1
        else:
            self.GUI.winColor = self.GUI.red
            self.winnerIndex = 2

        killCount = 0
        if loop:
            while killCount < 1000:
                self.GUI.update(self.board, ended= True)
                killCount += 1
        else:
            while True:
                self.GUI.update(self.board, ended= True)

    def deselect(self):
        #Unselect already selected
        for i in self.selected:
            self.board[i].selected = False
        self.selected = []

    def playSelected(self):
        #If there are two selected, play move
        if len(self.selected) == 2:
            #Play move
            mv = Move(self.board[self.selected[0]], self.board[self.selected[1]])
            if self.board.playMove(mv):
                #Deselect pieces

                self.deselect()
                return True
        return False

    def checkScore(self):
        #Create path counter variable
        pc = PC(self.board)
        #Find paths
        path1 = pc.findLongestColor(self.p1.color)
        path2 = pc.findLongestColor(self.p2.color)
        score = (len(path1), len(path2))
        self.score = score
        return score

    def endGame(self):
        self.done = True