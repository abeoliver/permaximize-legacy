"""
PlottedAnalysis.py
Permaximize
Abraham Oliver and Jadan Ercoli
"""

#Import libraries
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt

import read

global topPop, PATH
topPop = 142
PATH = "GameRecords\\Abe\\Debug\\A"

class WeightPlot:
    def __init__(self, name, weightNumber, numTypes = 5, 
                    combinedFunc = None, xAxis = "Weight"):
        """
        Object used for transporting data for plotting
        
        'name' = pot name
        'weightNumber' = which weight to calculate for
        'numTypes' = number of subsections of data (default = 5)
        """
        #Check weightNumber
        if weightNumber not in range(6): raise ValueError("Not a valid weight")
        self.weight = weightNumber
        
        #Check numTypes
        if numTypes < 1: raise ValueError("Not a valid number of subsections")
        self.numTypes = numTypes
        
        self.name = name
        self.data = []
        self.fitnesses = []
        
        self.xAxis = xAxis
        
        self.combinedFunc = combinedFunc
        if combinedFunc != None:
            self.combined = True
        else:
            self.combined = False
        
        #Calculate data and fitness
        self.getData()
    
    def getData(self, popnum = topPop):
        #Retrieve data list of all populations
        if popnum < 0: raise ValueError("Not a valid population number")
        self.finalIndex = popnum
        pops = []
        
        #List of all populations
        for i in range(self.finalIndex):
            loaded = read.pop(read.abe, "FINAL\\B" + str(i + 1))
            pops.append(loaded)
        #Sort population list
        pops = sorted(pops, key = lambda x: x.gen)

        #Get data items of the top 3 chromosomes from each population
        #Iterate through each population        
        for p in pops:
            #Take top 3 chromosomes
            p = sorted(p, key = lambda x: x.calcFitness(), reverse = True)
            for index in range(3):
                self.data.append(p[index])
        #Take fitnesses for every data point
        self.fitnesses = [x.calcFitness() for x in self.data]
    
    def weightData(self):
        weights = [x.data[self.weight] for x in self.data]
        return weights
    
    def getSubsets(self, data):
        plotSets = []
        x = data
        types = self.numTypes
        for i in range(types):
            if i == 0:
                plotSets.append(x[:len(x) / types])
            elif i == (types - 1):
                plotSets.append(x[(i * len(x)) / types:])
            else:
                plotSets.append(x[(i*len(x))/types : ((i+1)*len(x))/types])
        return plotSets
    
    def setCombined(self, secondWeight, cMode):
        self.weight2 = secondWeight
        self.cMode = cMode
        self.combined = True
    
    def combinedWeights(self, data1, data2, mode = '*'):
        """
        Returns list of x values in terms of data1 and data2 by mode
        
        Modes:
            '*' - Multiplication (default, or if)
            '/' - Division
            '+' - Addition
            '-' - Subtraction
        """
        if mode == '+':
            x = [x.data[data1] + x.data[data2] for x in self.data]
        elif mode == '-':
            x = [x.data[data1] - x.data[data2] for x in self.data]
        elif mode == '*':
            x = [x.data[data1] * x.data[data2] for x in self.data]
        elif mode == '/':
            x = [float(x.data[data1]) / x.data[data2] for x in self.data]
        else:
            raise ValueError("Not a valid mode")
        return x

class ChromosomeFigure:
    def __init__(self):
        #Color Variables
        self.cmap = ["red", "orange", "yellow",
                    "limegreen", "darkcyan"]
    
    def legend(self, numsets):
        patches = []
        labelList = self.labelNames(topPop, numsets)
        for i in range(numsets):
            p = mpatch.Patch(color = self.cmap[i], label = labelList[i])
            patches.append(p)
        legend = plt.legend(handles = patches, loc = 'upper right', shadow = True)
        legend.draggable(state = True)
        return legend
    
    def labelNames(self, length, sets):
        x = []
        for i in range(sets):
            if i == 0:
                ts1 = 1
            else:
                ts1 = (length / sets ) * i
            ts2 = (length / sets ) * (i + 1)
            s = "%i to %i" % (ts1, ts2)
            x.append(s)
        return x

    def createFig(self, name, size, *args):
        """
        Creates a figure for all the plots given in args
        
        'name' = super title
        'size' = tuple (number horizontal, number verticle)
        'args' = all datas
        """
        #Check arguments
        numFigs = len(args)
        if numFigs <= 0: raise RuntimeError("Not enough arguments")
        
        #Super variables
        self.fig = plt.figure(name)
        self.fig.suptitle(name, fontsize = 20)
        
        #Make plots for every data
        for index in range(len(args)):
            #Set necessary data
            plot = args[index]
            types = plot.numTypes
            if types <= 0: raise ValueError("Not a valid number of types")
            if plot.combined:
                if plot.combinedFunc == None:
                    xData = plot.combinedWeights(plot.weight, plot.weight2,
                                                plot.cMode)
                else:
                    xData = plot.combinedFunc(plot.data)
            else: xData = plot.weightData()
            yData = plot.fitnesses
            
            #Create subplot
            sub = plt.subplot(size[1], size[0], index + 1)
            sub.set_title(str(plot.name))
            
            #Plot data
            #Get subsets
            xSubs = plot.getSubsets(xData)
            ySubs = plot.getSubsets(yData)
            #Plot subsets
            sub.set_title(plot.name, fontsize = 15)
            sub.set_xlabel(plot.xAxis)
            sub.set_ylabel("Fitness")
            for i in range(len(xSubs)):
                sub.scatter(xSubs[i], ySubs[i], color = self.cmap[i])      

#=============================================================================
def SB():
    c = ChromosomeFigure()
    OSB = WeightPlot("Opponent Strategy Bonus", 0, 5)
    PSB = WeightPlot("Personal Strategy Bonus", 3, 5)
    CSB = WeightPlot("Destructive vs Constructive", 0, 5, xAxis = "Destructive / Constructive")
    CSB.setCombined(3, '/')
    c.createFig("Strategy Bonus", (3,1), OSB, PSB, CSB)

def CC():
    c = ChromosomeFigure()
    OCC = WeightPlot("Opponent Chain Subtraction", 1, 5)
    PCC = WeightPlot("Personal Chain Addition", 2, 5)
    CCC = WeightPlot("Destructive vs Constructive", 1, 5, xAxis = "Destructive / Constructive")
    CCC.setCombined(2, '/')
    c.createFig("Chain Changes", (3,1), OCC, PCC, CCC)

def PS():
    c = ChromosomeFigure()
    N = WeightPlot("Destructive", 5, 5)
    P = WeightPlot("Constructive", 4, 5)
    CNP = WeightPlot("Destructive vs Constructive", 5, 5, xAxis = "Destructive / Constructive")
    CNP.setCombined(4, '/')
    c.createFig("Destructive vs Constructive", (3,1), N, P, CNP)

def combineAll(data):
    final = []
    for c in data:
        w = c.data
        pos = w[4]* w[2] * w[3]
        neg = w[5]* w[0] * w[1]
        final.append(neg / float(pos))
    return final

def overall():
    c = ChromosomeFigure()
    S = WeightPlot("", 0, 5, combinedFunc = combineAll, xAxis = "Destructives / Constructives")
    c.createFig("Overall Destructive vs Constructive", (1,1), S)

#=============================================================================
def record():
    #Get list of populations
    pops = []
    for i in range(topPop):
        loaded = read.pop(PATH + str(i + 1))
        pops.append(loaded)
    #Sort population list
    pops = sorted(pops, key = lambda x: x.gen)
    
    #Get data for bar height (average score difference)
    data = []
    for p in pops:
        total = 0
        numToTake = 10
        #Take only 'numToTake' best
        for c in range(numToTake):
            total += p[c].lastScore
        data.append(float(total) / numToTake)
    
    #Plot bar
    xData = range(1,topPop + 1)
    fig = plt.figure("Average Score Difference")
    fig.suptitle("Average Score Difference", fontsize = 20)
    sub = plt.subplot(111)
    sub.set_xlabel("Population Number")
    sub.set_ylabel("Average Score Difference")
    for i in range(len(data)):
        if data[i] > 0:
            sub.bar(i+1, data[i], width = 1, color = "#2196F3")
        elif data[i] < 0:
            sub.bar(i+1, data[i], width = 1, color = "#f44336")
        else:
            sub.bar(i+1, 0, width = 1)

def printFitnesses():
    pops = []
    #List of all populations
    for i in range(topPop):
        loaded = read.pop(read.abe, "FINAL\\B" + str(i + 1))
        pops.append(loaded)
    #Sort population list
    pops = sorted(pops, key = lambda x: x.gen)

    #Print all fitnesses
    for i in range(topPop):
        pops[i] = sorted(pops[i], key = lambda x: x.calcFitness(), reverse = True)
        toPrint = ""
        for m in pops[i]:
            toPrint += str(m.fitness)
        print "%i :: %s" % (i, toPrint)

def fitnessChart():
    pops = []
    #List of all populations
    for i in range(topPop):
        loaded = read.pop(read.abe, "FINAL\\B" + str(i + 1))
        pops.append(loaded)
    #Sort population list
    pops = sorted(pops, key = lambda x: x.gen)
    for p in pops:
        sorted(p, key = lambda x: x.calcFitness())

    #Datas
    xData = range(1, len(pops) + 1)
    yData = [x[0].calcFitness() for x in pops]
    """
    for i in pops:
        total = 0
        for p in range(2):
            total += i[p].fitness
        yData.append(total / 2.0)
    """

    #Plot data
    plt.bar(xData, yData)
    
#Display Final
"""
SB()
CC()
PS()
overall()
printFitnesses()
"""
record()
plt.show()
