import numpy as np

from Hand import HAND_RANKINGS, SPECIAL_HANDS_NAMES, HandScore
from HandAnalysis import HandAnalysis
from unitTests import determineWinnerUnitTests

def printIndexeOfAllPossibleHands(shouldPrint=False):
    handScores = [HandScore(x) for x in HandAnalysis.constructAllPossibleHands()]
    scoreToIndexMap = {x: [] for x in HAND_RANKINGS + SPECIAL_HANDS_NAMES}
    for index,x in enumerate(handScores):
        scoreToIndexMap[x.score].append(index)
    
    if shouldPrint:
        for key,value in scoreToIndexMap.items():
            print(f"{key}: {value}")

    return scoreToIndexMap
        

def main() -> None:
    #Work In Progress
    #printIndexeOfAllPossibleHands(True)
    determineWinnerUnitTests(printIndexeOfAllPossibleHands(False))
    #testDetermineWinner()
    
if __name__ == "__main__":
    main()