from HandAnalysis import HandAnalysis


def determineWinnerUnitTests(scoreToIndexListMap):
    hands = HandAnalysis.constructAllPossibleHands()
    selectHandBasedOnIndexes = lambda indexes: [hands[x] for x in indexes]
    
    def assertOn1dList(expectedList, acutalList, msg=""):
        assert len(expectedList) == len(acutalList), msg
        for x,y in zip(expectedList, acutalList):
            assert x == y, msg
    
    def getHandIndexesBasedOnHandScore(listHandScores):
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