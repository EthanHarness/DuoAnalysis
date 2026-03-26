PRIME_PAIR_NAME = "PrimePair"
SUP_PAIR_NAME = "SuperiorPair"

JUDGE_NAME = "Judge"
WARDEN_NAME = "Warden"
HIGH_WARDEN_NAME = "HighWarden"
EXECUTOR_NAME = "Executor"
SPECIAL_HANDS_NAMES = [
    JUDGE_NAME,
    WARDEN_NAME,
    HIGH_WARDEN_NAME,
    EXECUTOR_NAME
]

ONE_TWO_NAME = "OneTwo"
ONE_FOUR_NAME = "OneFour"
ONE_NINE_NAME = "OneNine"
ONE_TEN_NAME = "OneTen"
FOUR_TEN_NAME = "FourTen"
FOUR_SIX_NAME = "FourSix"
NON_PAIR_NAMES = [
    ONE_TWO_NAME,
    ONE_FOUR_NAME,
    ONE_NINE_NAME, 
    ONE_TEN_NAME,
    FOUR_TEN_NAME,
    FOUR_SIX_NAME
]

PAIR_10_NAME = "10Pair"
PAIR_9_NAME = "9Pair"
PAIR_8_NAME = "8Pair"
PAIR_7_NAME = "7Pair"
PAIR_6_NAME = "6Pair"
PAIR_5_NAME = "5Pair"
PAIR_4_NAME = "4Pair"
PAIR_3_NAME = "3Pair"
PAIR_2_NAME = "2Pair"
PAIR_1_NAME = "1Pair"
PAIR_LIST_NAMES = [
    PAIR_10_NAME,
    PAIR_9_NAME,
    PAIR_8_NAME,
    PAIR_7_NAME,
    PAIR_6_NAME,
    PAIR_5_NAME,
    PAIR_4_NAME,
    PAIR_3_NAME,
    PAIR_2_NAME,
    PAIR_1_NAME
]

POINT_9_NAME = "Points9"
POINT_8_NAME = "Points8"
POINT_7_NAME = "Points7"
POINT_6_NAME = "Points6"
POINT_5_NAME = "Points5"
POINT_4_NAME = "Points4"
POINT_3_NAME = "Points3"
POINT_2_NAME = "Points2"
POINT_1_NAME = "Points1"
POINT_0_NAME = "Points0"
POINT_NAME_LIST = [
    POINT_9_NAME,
    POINT_8_NAME,
    POINT_7_NAME,
    POINT_6_NAME,
    POINT_5_NAME,
    POINT_4_NAME,
    POINT_3_NAME,
    POINT_2_NAME,
    POINT_1_NAME,
    POINT_0_NAME
]

HAND_RANKINGS = [PRIME_PAIR_NAME, SUP_PAIR_NAME] + PAIR_LIST_NAMES + NON_PAIR_NAMES + POINT_NAME_LIST

def getPointNameBasedOnVal(val):
    match val:
        case 0: return POINT_0_NAME
        case 1: return POINT_1_NAME
        case 2: return POINT_2_NAME
        case 3: return POINT_3_NAME
        case 4: return POINT_4_NAME
        case 5: return POINT_5_NAME
        case 6: return POINT_6_NAME
        case 7: return POINT_7_NAME
        case 8: return POINT_8_NAME
        case 9: return POINT_9_NAME

def getPairNameBasedOnVal(val):
    match val:
        case 1: return PAIR_1_NAME
        case 2: return PAIR_2_NAME
        case 3: return PAIR_3_NAME
        case 4: return PAIR_4_NAME
        case 5: return PAIR_5_NAME
        case 6: return PAIR_6_NAME
        case 7: return PAIR_7_NAME
        case 8: return PAIR_8_NAME
        case 9: return PAIR_9_NAME
        case 10: return PAIR_10_NAME

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
    

class HandScore:
    def __init__(self, hand: Hand):
        self.hand: Hand = hand
        self.score = self.getHandScore()
        self.specialHand = False
        if self.score in SPECIAL_HANDS_NAMES: self.specialHand = True

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
        if self.getIsPrimePair(): return PRIME_PAIR_NAME
        if self.getIsSuperiorPair(): return SUP_PAIR_NAME
        if self.getIsExecutor(): return EXECUTOR_NAME
        
        if self.getIsPair():
            v1, _ = self.getHandVals()
            return getPairNameBasedOnVal(v1)
        
        if self.getIsJudge(): return JUDGE_NAME
        if self.getIsHighWarden(): return HIGH_WARDEN_NAME
        if self.getIsWarden(): return WARDEN_NAME
        if self.getIsOneTwo(): return ONE_TWO_NAME
        if self.getIsOneFour(): return ONE_FOUR_NAME
        if self.getIsOneNine(): return ONE_NINE_NAME
        if self.getIsOneTen(): return ONE_TEN_NAME
        if self.getIsFourTen(): return FOUR_TEN_NAME
        if self.getIsFourSix(): return FOUR_SIX_NAME

        return getPointNameBasedOnVal(self.getPoints())
    
    @staticmethod
    def specialHandsThatInteractWithAGivenScore(score): #returns the special hands that have interactions with some score
        if score == PRIME_PAIR_NAME: return []
        if score == SUP_PAIR_NAME: return [EXECUTOR_NAME]
        if score == PAIR_10_NAME: return []
        if "Pair" in score: return [JUDGE_NAME, HIGH_WARDEN_NAME, WARDEN_NAME]
        return [WARDEN_NAME, HIGH_WARDEN_NAME]