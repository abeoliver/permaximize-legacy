#matingHistory.py
#Game
#Abraham Oliver and Jadan Ercoli

class History (object):
    def __init__(self, originalData):
        self.origin = originalData
        self.history = [originalData]
        self.partners = []

    def preMate(self, partner):
        #New partner data
        if type(partner) == list:
            self.partners.append(partner)
        else:
            self.partners.append(partner.data)

    def postMate(self, newSelf):
        self.history.append(newSelf.data)

    def __str__(self):
        pass

    def printData(self):
        print("Data progression for Chromosome:")
        for i in range(len(self.history)):
            print("#%i :: %s" % (i, str(self.history[i])))

    def printMate(self):
        print("\nMate progression for Chromosome:")
        for i in range(len(self.partners)):
            print("SELF :: " + str(self.history[i]))
            print("PART :: " + str(self.partners[i]))
            print("")
            if i == len(self.partners) - 1:
                print("-----------------------")
                print("FINAL :: " + str(self.history[len(self.history) - 1]))