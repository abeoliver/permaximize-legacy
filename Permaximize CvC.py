# Permaximize CvC.py
# Game
# Plexivate Software 2016

# Plays a permaximize game with a human vs a human
from AI.aiDesigned import Player as AI
from PlayPermaximize import Game

while True:
    p = Game(AI(), AI())
    p.play(loop = True)
