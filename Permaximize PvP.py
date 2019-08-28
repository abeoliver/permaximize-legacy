# Permaximize PvP.py
# Game
# Plexivate Software 2016

# Plays a permaximize game with a human vs a human
from GamePieces.player import Player
from PlayPermaximize import Game

p = Game(Player(), Player())
p.play()