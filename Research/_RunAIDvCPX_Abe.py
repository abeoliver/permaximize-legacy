#_RunAIDvCPX.py
#Game
#Abraham Oliver and Jadan Ercoli

from AI.aiDesigned import Player
from cpxChromosome import Chromosome
from genTournament import *

#Function to load previous populations
"""
def load(path, name, toPop):
    p = Read.pop(path, name)
    m = []
    for i in p:
        try: new = i.copy()
        except: new = i
        m.append(new)
    toPop.members = m
    toPop.record = p.record
    toPop.genCount = p.genCount

#Load Previous
load(filePath, "A588", t.pop1)
load(filePath, "B588", t.pop2)
"""

#Begin tournament
abe = "GameRecords\\Abe\\Debug\\"
jadan = "GameRecords\\Jadan\\"
#TODO Change back to 10
t = Tournament(10, abe, Chromosome, Player)
t.play(3)
