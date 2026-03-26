import numpy as np
from Hand import EXECUTOR_NAME, HAND_RANKINGS, HIGH_WARDEN_NAME, JUDGE_NAME, \
    PAIR_10_NAME, PRIME_PAIR_NAME, SUP_PAIR_NAME, WARDEN_NAME, Hand, HandScore, Stick

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
        bestHandScore = HAND_RANKINGS[min([HAND_RANKINGS.index(x.score) for x in regHands])]
        bestRegHands = [x for x in regHands if x.score == bestHandScore]
        bestHandInteractions = HandScore.specialHandsThatInteractWithAGivenScore(bestHandScore)
        specialHandInteractions = [x for x in specialHands if x.score in bestHandInteractions]
        
        if bestHandScore == PRIME_PAIR_NAME: return bestRegHands
        if bestHandScore == SUP_PAIR_NAME and len(specialHandInteractions) != 0: return specialHandInteractions
        if bestHandScore == SUP_PAIR_NAME: return bestRegHands
        
        #Assuming no interaction with Warden
        #Assuming no interaction with Judge
        if bestHandScore == PAIR_10_NAME: return bestRegHands

        #Best hand is a non 10 pair logic
        #Assuming judge wins if you have non 10 pair, high warden/warden, and judge
        #Assuming high warden and pair rematch if pair, high warden, warden
        if "Pair" in bestHandScore:
            judgeList = [x for x in specialHandInteractions if x.score == JUDGE_NAME]
            hWList = [x for x in specialHandInteractions if x.score == HIGH_WARDEN_NAME]
            if len(judgeList) != 0: return judgeList
            if len(hWList) != 0: return hWList + bestRegHands #no judge so rematch the pair hW's
            
            #Only warden left in specialHandInteractions so compute pair points and compare against warden points(3)
            pairPoints = bestRegHands[0].getPoints()
            if pairPoints > 3: return bestRegHands
            return specialHandInteractions

        #Non points with best being 1-2
        #Assuming highWarden and non warden best hand rematch even if warden is in special hand list
        if not onlyPoints:
            highWardenList = [x for x in specialHandInteractions if x.score == HIGH_WARDEN_NAME]
            if len(highWardenList) != 0: return highWardenList + bestRegHands
            return specialHandInteractions + bestRegHands #Only option is for warden interactions which always rematch since its a non point hand
        
        #Only hands left are point hands
        #Need to evaluate that best hand has more points then rest of specials with no interaction (judge/executor)
        if len(specialHandInteractions) == 0: 
            relaventHands = specialHands + bestRegHands
            maxPoints = max([x.getPoints() for x in relaventHands])
            return [x for x in relaventHands if x.getPoints() == maxPoints]
        
        executorList = [x for x in specialHands if x.score == EXECUTOR_NAME]
        judgeList = [x for x in specialHands if x.score == JUDGE_NAME]
        highWardenList = [x for x in specialHands if x.score == HIGH_WARDEN_NAME]
        wardenList = [x for x in specialHands if x.score == WARDEN_NAME]
        
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