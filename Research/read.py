#Read.py
#Game
#Abraham Oliver and Jadan Ercoli
"""Read storage files, population files, and quick test"""

import random as R

import analysis as A
import basePopulation as P
import cpxChromosome as CPX

global exceptions
exceptions = (SyntaxError, IOError)

#File Paths
global abe, jadan
abe = "GameRecords\\Abe\\A"
jadan = "GameRecords\\Jadan\\A"

def pop(pathName):
        pop = P.Population(1, CPX.Chromosome)
        try:
                pop = pop.loadPop(pathName)
        except exceptions:
                print "File couldn't be retrieved"
                return None
        return pop

def allPops(path,num):
        return [pop(path + str(i + 1)) for i in range(num)]

def storage(path):
        stor = A.Storage(path)
        try:
                stor = stor.load()
        except exceptions:
                print "File couldn't be retrieved"
                return None
        return stor

def randomGames(number, storage):
        games = []
        reps = []
        for i in range(number):
                index = R.randint(0, len(storage.games) - 1)
                #If alread in the list
                while storage[index] in games:
                        index = R.randint(0, len(storage.games) - 1)
                r = A.Replay(storage[index])
                reps.append(r)
        return reps

        
