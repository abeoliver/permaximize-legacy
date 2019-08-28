# Permaximize PvP.py
# Game
# Plexivate Software 2016

# Plays a permaximize game with a human vs a human
from random import shuffle

from AI.aiDesigned import Player as AI
from GamePieces.player import Player
from PlayPermaximize import Game

players = [Player(), AI()]
shuffle(players)
p = Game(players[0], players[1])
p.play()
