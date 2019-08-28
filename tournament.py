# tournament.py
# Game
# Plexivate Software, 2016

from random import shuffle

from GamePieces.player import Player as Base
from PlayPermaximize import Game


class Round (object):
    def __init__(self, players, level):
        self.players = players
        # Randomize Matchups
        self.players = shuffle(self.players)
        # What level in tournament
        self.level = level
        # Was bye used?
        self.bye = False
        #Winners
        self.winners = []

    def play(self):
        # Match up opponents, set self.bye if bye is used
        if len(self.players) % 2 != 0: self.bye = true
        for i in range(len(self.players) / 2):
            # Choose players
            p1 = self.players.pop()
            p2 = self.players.pop()

            # Play games
            game = Game(p1, p2, guiClass = None)
            game.play()

            # Save winner
            if game.winnerIndex == 1:
                self.winners.append(p1)
                p2.lastRound = self.level
            elif game.winnerIndex == 2:
                self.winners.append(p2)
                p1.lastRound = self.level

class Tournament (object):
    def __init__(self):
        pass

    def play(self):
        pass

class Player (Base):
    def __init__(self, name, passcode, record, lastRound):
        super(Player, self).__init__()
        self.name = name
        self.passcode = passcode
        self.record = record
        self.lastRound = lastRound