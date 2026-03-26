import numpy as np

class Stick:
    def __init__(self, inputStickComponentList):
        self.val = inputStickComponentList[0]
        self.color = inputStickComponentList[1]

    def createString(self):
        return f"{self.val} {self.color}"

class Hand:
    def __init__(self, stick1: Stick, stick2: Stick):
        self.showingStick = stick1 
        self.hiddenStick = stick2 

    def isMonochromeRed(self):
        return True if self.showingStick.color == 'red' and self.hiddenStick.color == 'red' else False
    
    def printHand(self):
        return f"{self.showingStick.createString()} {self.hiddenStick.createString()}"

pairStrengths = [f"{x}Pair" for x in range(10, -1, -1)]
pointStrengths = [f"Points{x}" for x in range(9, -1, 0)]
handRankings = ["PrimePair", "SuperiorPair"] + pairStrengths + \
    ["OneTwo", "OneFour", "OneNine", "OneTen", "FourTen", "OneSix"] + pointStrengths

class HandScore:
    def __init__(self, hand: Hand):
        self.hand: Hand = hand
        self.score = self.getHandScore()

    def getHandVals(self):
        return (self.hand.showingStick.val, self.hand.hiddenStick.val)

    def getIsPrimePair(self):
        if not self.hand.isMonochromeRed(): return False
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [3,8])
    
    def getIsSuperiorPair(self):
        if not self.hand.isMonochromeRed(): return False
        v1, v2 = self.getHandVals()
        if self.evaluateValsAgainstList(v1, v2, [1,3]): return True
        if self.evaluateValsAgainstList(v1, v2, [1,8]): return True
        return False
    
    def getIsExecutor(self):
        if not self.hand.isMonochromeRed(): return False
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [4,7])
    
    def getIsJudge(self):
        v1, v2 = self.getHandVals 
        return self.evaluateValsAgainstList(v1, v2, [3,7])
    
    def getIsPair(self):
        v1, v2 = self.getHandVals()
        return v1 == v2
    
    def getIsHighWarden(self):
        if not self.hand.isMonochromeRed(): return False
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [9, 4])
    
    def getIsWarden(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [9, 4])
    
    def getIsOneTwo(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [1, 2])
    
    def getIsOneFour(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [1, 4])
    
    def getIsOneNine(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [1, 9])
    
    def getIsOneTen(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [1, 10])
    
    def getIsFourTen(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [4, 10])
    
    def getIsFourSix(self):
        v1, v2 = self.getHandVals()
        return self.evaluateValsAgainstList(v1, v2, [4, 6])
    
    def getPoints(self):
        v1, v2 = self.getHandVals()
        return (v1 + v2) % 10
    
    def evaluateValsAgainstList(self, v1, v2, l1):
        if v1 not in l1 and v2 not in l1: return False
        return True
    
    def getHandScore(self):
        if self.getIsPrimePair(): return "PrimePair"
        if self.getIsSuperiorPair(): return "SuperiorPair"
        if self.getIsExecutor(): return "Executor"
        
        if self.getIsPair():
            v1, _ = self.getHandVals()
            return f"{v1}Pair"
        
        if self.getIsJudge(): return "Judge"
        if self.getIsHighWarden(): return "HighWarden"
        if self.getIsWarden(): return "Warden"
        if self.getIsOneTwo(): return "OneTwo"
        if self.getIsOneFour(): return "OneFour"
        if self.getIsOneNine(): return "OneNine"
        if self.getIsOneTen(): return "OneTen"
        if self.getIsFourTen(): return "FourTen"
        if self.getIsFourSix(): return "OneSix"
        return f"Points{self.getPoints()}"

class HandAnalysis: 
    def __init__(self):
        pass

    @staticmethod
    def constructAllPossibleHands():
        colors = np.array(['red', 'yellow'])
        nums = np.arange(1,11)
        
        allSticks = np.transpose([np.repeat(colors, len(nums)), np.tile(nums, len(colors))])
        allHands = np.empty(380, dtype=object)
        allSticksSize = len(allSticks)
        
        count = 0
        for index1, stick1L in enumerate(allSticksSize):
            for index2, stick2L in enumerate(allSticksSize):
                if index1 == index2: continue

                hand = Hand(Stick(stick1L), Stick(stick2L))
                allHands[count] = hand
                count += 1

        return allHands

def main() -> None:
    #Work In Progress
    HandAnalysis.constructAllPossibleHands() 

if __name__ == "__main__":
    main()