from typing import List
import numpy as np

class Stick:
    def __init__(self, inputStickComponentList):
        self.val = int(inputStickComponentList[1])
        self.color = inputStickComponentList[0]

    def createString(self):
        return f"{self.color} {self.val}"

class Hand:
    def __init__(self, stick1: Stick, stick2: Stick):
        self.showingStick = stick1 
        self.hiddenStick = stick2 

    def isMonochromeRed(self):
        return True if self.showingStick.color == 'red' and self.hiddenStick.color == 'red' else False
    
    def printHand(self):
        return f"{self.showingStick.createString()} {self.hiddenStick.createString()}"

pairStrengths = [f"{x}Pair" for x in range(10, 0, -1)]
pointStrengths = [f"Points{x}" for x in range(9, -1, -1)]
handRankings = ["PrimePair", "SuperiorPair"] + pairStrengths + \
    ["OneTwo", "OneFour", "OneNine", "OneTen", "FourTen", "FourSix"] + pointStrengths
specialHandList = ["Judge", "Warden", "HighWarden", "Executor"]

#Should be a part of Hand or make methods static
class HandScore:
    def __init__(self, hand: Hand):
        self.hand: Hand = hand
        self.score = self.getHandScore()
        self.specialHand = False
        if self.score in specialHandList: self.specialHand = True

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
        v1, v2 = self.getHandVals() 
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
        if v1 not in l1 or v2 not in l1: return False
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
        if self.getIsFourSix(): return "FourSix"
        return f"Points{self.getPoints()}"
    
    @staticmethod
    def specialHandsThatInteractWithAGivenScore(score): #returns the special hands that have interactions with some score
        if score == "PrimePair": return []
        if score == "SuperiorPair": return ["Executor"]
        if score == "10Pair": return []
        if "Pair" in score: return ["Judge", "HighWarden", "Warden"]
        return ["Warden", "HighWarden"]
    

class HandAnalysis: 
    def __init__(self):
        pass

    @staticmethod
    def constructAllPossibleHands():
        colors = np.array(['red', 'yellow'])
        nums = np.arange(1,11)
        
        allSticks = np.transpose([np.repeat(colors, len(nums)), np.tile(nums, len(colors))])
        allHands = np.empty(380, dtype=object)
        
        count = 0
        for index1, stick1L in enumerate(allSticks):
            for index2, stick2L in enumerate(allSticks):
                if index1 == index2: continue

                hand = Hand(Stick(stick1L), Stick(stick2L))
                allHands[count] = hand
                count += 1

        return allHands.tolist()
    
    @staticmethod
    def onlyPointHands(nonSpecialHands):
        for x in nonSpecialHands:
            if not "Points" in x.score: return False
        return True

    #TODO: Verify certain assumptions consistent with game (mostly related to warden and high warden hands)
    @staticmethod
    def determineHandWinner(handList): #Takes in a list of hands and outputs the winner/winners (in case of draw)
        handScores = [HandScore(x) for x in handList]

        specialHands = [x for x in handScores if x.specialHand == True]
        regHands = [x for x in handScores if x.specialHand == False]

        #Might need to change based on actual warden v high warden logic
        if len(regHands) == 0: #If regHands is empty then can just calculate points of all special hands and find highest
            maxPoints = max([x.getPoints() for x in specialHands])
            bestHands = [x for x in specialHands if x.getPoints() == maxPoints]
            return bestHands
        
        
        #First find best hand excluding special hands
        onlyPoints = HandAnalysis.onlyPointHands(regHands)
        bestHandScore = handRankings[min([handRankings.index(x.score) for x in regHands])]
        bestRegHands = [x for x in regHands if x.score == bestHandScore]
        bestHandInteractions = HandScore.specialHandsThatInteractWithAGivenScore(bestHandScore)
        specialHandInteractions = [x for x in specialHands if x.score in bestHandInteractions]
        
        if bestHandScore == "PrimePair": return bestRegHands
        if bestHandScore == "SuperiorPair" and len(specialHandInteractions) != 0: return specialHandInteractions
        if bestHandScore == "SuperiorPair": return bestRegHands
        
        #Assuming no interaction with Warden
        #Assuming no interaction with Judge
        if bestHandScore == "10Pair": return bestRegHands

        #Best hand is a non 10 pair logic
        #Assuming judge wins if you have non 10 pair, high warden/warden, and judge
        #Assuming high warden and pair rematch if pair, high warden, warden
        if "Pair" in bestHandScore:
            judgeList = [x for x in specialHandInteractions if x.score == "Judge"]
            hWList = [x for x in specialHandInteractions if x.score == "HighWarden"]
            if len(judgeList) != 0: return judgeList
            if len(hWList) != 0: return hWList + bestRegHands #no judge so rematch the pair hW's
            
            #Only warden left in specialHandInteractions so compute pair points and compare against warden points(3)
            pairPoints = bestRegHands[0].getPoints()
            if pairPoints > 3: return bestRegHands
            return specialHandInteractions

        #Non points with best being 1-2
        #Assuming highWarden and non warden best hand rematch even if warden is in special hand list
        if not onlyPoints:
            highWardenList = [x for x in specialHandInteractions if x.score == "HighWarden"]
            if len(highWardenList) != 0: return highWardenList + bestRegHands
            return specialHandInteractions + bestRegHands #Only option is for warden interactions which always rematch since its a non point hand
        
        #Only hands left are point hands
        #Need to evaluate that best hand has more points then rest of specials with no interaction (judge/executor)
        if len(specialHandInteractions) == 0: 
            relaventHands = specialHands + bestRegHands
            maxPoints = max([x.getPoints() for x in relaventHands])
            return [x for x in relaventHands if x.getPoints() == maxPoints]
        
        executorList = [x for x in specialHands if x.score == "Executor"]
        judgeList = [x for x in specialHands if x.score == "Judge"]
        highWardenList = [x for x in specialHands if x.score == "HighWarden"]
        wardenList = [x for x in specialHands if x.score == "Warden"]
        
        #Could have the case where executor is the best point hand with warden/highWardens being in play
        if bestRegHands[0].getPoints() == 0 and len(executorList) != 0:
            if len(highWardenList) != 0: return highWardenList + executorList
            if len(wardenList) != 0: return executorList + wardenList
            return executorList
        
        if bestRegHands[0].getPoints() == 0 and len(judgeList) != 0:
            if len(highWardenList) != 0: return highWardenList + judgeList + bestRegHands
            if len(wardenList) != 0: return judgeList + wardenList + bestRegHands
            return bestRegHands + judgeList

        #Only interaction left is point hand vs warden/highWarden
        #Assuming high warden rematches points even if there is a warden
        if len(highWardenList) != 0: return highWardenList + bestRegHands
        return specialHandInteractions + bestRegHands
        

def printIndexeOfAllPossibleHands(shouldPrint=False):
    handScores = [HandScore(x) for x in HandAnalysis.constructAllPossibleHands()]
    scoreToIndexMap = {x: [] for x in handRankings + specialHandList}
    for index,x in enumerate(handScores):
        scoreToIndexMap[x.score].append(index)
    
    if shouldPrint:
        for key,value in scoreToIndexMap.items():
            print(f"{key}: {value}")

    return scoreToIndexMap

def determineWinnerUnitTests():
    hands = HandAnalysis.constructAllPossibleHands()
    scoreToIndexListMap = printIndexeOfAllPossibleHands(False)
    selectHandBasedOnIndexes = lambda indexes: [hands[x] for x in indexes]
    
    def assertOn1dList(expectedList, acutalList, msg=""):
        assert len(expectedList) == len(acutalList), msg
        for x,y in zip(expectedList, acutalList):
            assert x == y, msg
    
    def getHandIndexesBasedOnHandScore(listHandScores: List[HandScore]):
        indexes = []
        for handScore in listHandScores:
            score = handScore.score
            for potentialHandIndex in scoreToIndexListMap[score]:
                if hands[potentialHandIndex].printHand() == handScore.hand.printHand(): 
                    indexes.append(potentialHandIndex)
                    break
        indexes.sort()
        return indexes

    #Ensure that expectedWinners is sorted
    def runTest(handIndexes, expectedWinnerIndexes, failureMessage):
        winners = HandAnalysis.determineHandWinner(selectHandBasedOnIndexes(handIndexes))
        actualWinnerIndexes = getHandIndexesBasedOnHandScore(winners)
        assertOn1dList(expectedWinnerIndexes, actualWinnerIndexes, failureMessage)

    def testPrimePairHands():
        msg = "Prime Pair Testing Failed"
        indexes = [44, 135, 1, 64, 62, 43, 74, 25]
        expectedWinners = [44, 135]
        runTest(indexes, expectedWinners, msg)

        print("Prime Pair Tests passed")

    def testSuperiorPairHands():
        msg = "Superior Pair Testing Failed"
        indexes = [1, 189, 169, 0, 16, 43, 74, 64]
        expectedWinners = [1]
        runTest(indexes, expectedWinners, msg)

        indexes = [1, 6, 38, 133, 189, 169, 0, 16, 43, 74, 64, 62]
        expectedWinners = [62]
        runTest(indexes, expectedWinners, msg)

        indexes = [44, 1, 6, 38, 133, 189, 169, 0, 16, 43, 74, 64, 62]
        expectedWinners = [44]
        runTest(indexes, expectedWinners, msg)

        print("Superior Pair Tests passed")

    def testTenPair():
        msg = "10 Pair Testing Failed"
        indexes = [189, 370, 169, 9, 0, 61, 16, 25]
        expectedWinners = [189, 370]
        runTest(indexes, expectedWinners, msg)

        indexes = [189, 370, 169, 9, 0, 61, 16, 25, 43, 74, 64, 62]
        expectedWinners = [189, 370]
        runTest(indexes, expectedWinners, msg)

        print("10 Pair Tests passed")

    def testLowerPairs():
        msg = "Non 10 Pair Testing Failed"
        indexes = [169, 350, 9, 0, 61, 16, 25, 62]
        expectedWinners = [169, 350]
        runTest(indexes, expectedWinners, msg)

        indexes = [169, 350, 9, 0, 61, 16, 25, 74, 64, 62]
        expectedWinners = [64, 169, 350]
        runTest(indexes, expectedWinners, msg)

        indexes = [169, 350, 9, 0, 61, 16, 25, 74, 62]
        expectedWinners = [169, 350]
        runTest(indexes, expectedWinners, msg)

        indexes = [29, 9, 0, 61, 16, 25, 74, 62]
        expectedWinners = [29]
        runTest(indexes, expectedWinners, msg)

        indexes = [89, 9, 0, 61, 16, 25, 74, 62]
        expectedWinners = [74]
        runTest(indexes, expectedWinners, msg)

        print("Non 10 Pair Tests passed")

    def testNonPairs():
        msg = "Non 10 Pair Testing Failed"
        indexes = [0, 2, 61, 16, 25]
        expectedWinners = [0]
        runTest(indexes, expectedWinners, msg)

        indexes = [0, 2, 61, 16, 25, 43, 62]
        expectedWinners = [0]
        runTest(indexes, expectedWinners, msg)

        indexes = [0, 2, 61, 16, 25, 43, 62, 64]
        expectedWinners = [0, 64]
        runTest(indexes, expectedWinners, msg)

        indexes = [0, 2, 61, 16, 25, 43, 62, 64, 74]
        expectedWinners = [0, 64]
        runTest(indexes, expectedWinners, msg)

        indexes = [0, 2, 61, 16, 25, 43, 62, 74]
        expectedWinners = [0, 74]
        runTest(indexes, expectedWinners, msg)

        print("Non Pair Tests Passed")

    def testPoints():
        msg = "Point Testing Failed"
        indexes = [16, 24, 5, 15, 11, 25]
        expectedWinners = [16, 24]
        runTest(indexes, expectedWinners, msg)

        indexes = [16, 24, 5, 15, 11, 25, 43, 62]
        expectedWinners = [16, 24]
        runTest(indexes, expectedWinners, msg)

        indexes = [25, 43, 62]
        expectedWinners = [62]
        runTest(indexes, expectedWinners, msg)

        indexes = [25, 43]
        expectedWinners = [25, 43]
        runTest(indexes, expectedWinners, msg)

        indexes = [25, 43, 74, 64]
        expectedWinners = [25, 43, 64]
        runTest(indexes, expectedWinners, msg) #FIX

        indexes = [25, 43, 74, 64, 11]
        expectedWinners = [11, 64]
        runTest(indexes, expectedWinners, msg)

        indexes = [25, 43, 74, 11]
        expectedWinners = [11, 74]
        runTest(indexes, expectedWinners, msg)

        print("Point testing passed")

    testPrimePairHands()
    testSuperiorPairHands()
    testTenPair()
    testLowerPairs()
    testNonPairs()
    testPoints()
        

def main() -> None:
    #Work In Progress
    #printIndexeOfAllPossibleHands(True)
    determineWinnerUnitTests()
    #testDetermineWinner()
    
if __name__ == "__main__":
    main()