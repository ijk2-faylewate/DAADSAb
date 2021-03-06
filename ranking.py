import csv
import tennisTools
import sortLists
import worldSpecific

copyForSortOverallRank = []
copyForSortRankForRound = []
#copyForRankPointDifficulty = []
worldFile = worldSpecific.sendPath
#Update's total, season wide, points
def updateRankPoints(tornementName, roundNumber, gender):
    worldFile = worldSpecific.sendPath

    currentWinners = tennisTools.currentWinners
    rankPoints = 0
    previousRoundPoints = 0
    difficultyPoints = 0.0

    tempPlayerList = []
    playerList = []
    tempDataList = []
    pointsList = []

    tempBaseScores = tennisTools.copyForRankPointDifficulty

    #assign tornement difficulty
    if tornementName == tennisTools.tornementOne:
        difficultyPoints = 2.7
    elif tornementName == tennisTools.tornementTwo:
        difficultyPoints = 2.3
    elif tornementName == tennisTools.tornementThree:
        difficultyPoints = 3.1
    elif tornementName == tennisTools.tornementFour:
        difficultyPoints = 3.25

    #select ranking points for current rount and previous round
    with open('parameters\RANKING_POINTS.csv', "r") as readPoints:
        pointsReader = list(csv.reader(readPoints, delimiter =',', quotechar='|'))

    if gender == 'f':
        overallPointsFile = worldFile + 'playerStates\OVERALL_POINTS_WOMEN.csv'
    elif gender == 'm':
        overallPointsFile = worldFile + 'playerStates\OVERALL_POINTS_MEN.csv'

    #Points assigned to different rounds
    if roundNumber == '1':
        rankPoints = pointsReader[8][0]
    elif roundNumber == '2':
        rankPoints = pointsReader[4][0]
        previousRoundPoints = pointsReader[8][0]
    elif roundNumber == '3':
        rankPoints = pointsReader[3][0]
        previousRoundPoints = pointsReader[4][0]
    elif roundNumber == '4':
        rankPoints = pointsReader[1][0]
        previousRoundPoints = pointsReader[3][0]
    elif roundNumber == '5':
        rankPoints = pointsReader[0][0]
        previousRoundPoints = pointsReader[0][0]

    #Total points awarded to player leaving a round
    rankPoints = float(rankPoints) * difficultyPoints

    #Points deleted from player progressing to next round (new points added at next level)
    winnersDeduction = float(previousRoundPoints) * difficultyPoints

    #Read saved overall points into list
    with open(overallPointsFile, "r") as pointsFile:
        thesePlayers = csv.reader(pointsFile, delimiter=',', quotechar='|')
        for players in thesePlayers:
            tempDataList.append(players)

    #Populate temporary full player list
    for i in range(len(tempDataList)):
        playerList.append(tempDataList[i][0])

    #save temp list of winners
    tempPlayerListWinners = [tempPlayerList for tempPlayerList in playerList if tempPlayerList in currentWinners]
    #print(tempBaseScores)
    #Add points from round one. Then, add points if player not advancing, remove points if player advancing. Simply assign points to winner.
    for i in range(len(tempDataList)):
        for j in range(len(currentWinners)):
            if roundNumber == '1':
                if  currentWinners[j] == tempBaseScores[i][0]: #currentWinners[j] == tempDataList[i][0]:
                    baseByDiff = float(tempBaseScores[i][1]) * difficultyPoints
                    tempScore = float(tempDataList[i][1])
                    tempDataList[i].insert(1, float(tempScore) + baseByDiff)
                    tempDataList[i].pop(2)

            elif roundNumber == '5':
                if tempPlayerListWinners[j] == tempBaseScores[i][0]:
                    baseByDiff = float(tempBaseScores[i][1]) * difficultyPoints
                    tempScore = float(tempDataList[i][1])
                    tempDataList[i].insert(1, baseByDiff)
                    tempDataList[i].pop(2)

            else:
                if tempPlayerListWinners[j] == tempBaseScores[i][0]:
                    baseByDiff = float(tempBaseScores[i][1]) * difficultyPoints
                    tempScore = float(tempDataList[i][1])
                    tempDataList[i].insert(1, baseByDiff)
                    tempDataList[i].pop(2)

    #Save points back into file
    with open(overallPointsFile, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(tempDataList)):
            writePoints.writerow(tempDataList[players])

    #Copy list for eventual display of rank
    global copyForSortOverallRank
    copyForSortOverallRank = tempDataList

#Calculates points within a tornement, round to round. Saves information to a temporary location, in case of mid tornement closure.
def updatePointsCurrentTornement(tornementName, roundNumber, gender):
    #Shared variables/globals
    worldFile = worldSpecific.sendPath
    currentWinners = tennisTools.currentWinners
    currentWinnersScoreMargin = tennisTools.currentWinnersScoreMargin

    rankPoints = 0
    #previousRoundPoints = 0

    playerList = []
    tempDataList = []

    #select ranking points for current round and previous round
    with open('parameters\RANKING_POINTS.csv', "r") as readPoints:
        pointsReader = list(csv.reader(readPoints, delimiter =',', quotechar='|'))

    #Points assigned to different rounds
    if roundNumber == '1':
        rankPoints = int(pointsReader[8][0])
    elif roundNumber == '2':
        rankPoints = pointsReader[4][0]
        #previousRoundPoints = int(pointsReader[8][0])
    elif roundNumber == '3':
        rankPoints = pointsReader[3][0]
        #previousRoundPoints = int(pointsReader[4][0])
    elif roundNumber == '4':
        rankPoints = pointsReader[1][0]
        ##previousRoundPoints = int(pointsReader[3][0])
    elif roundNumber == '5':
        rankPoints = pointsReader[0][0]
        #previousRoundPoints = int(pointsReader[0][0])

    #Select gender of files
    if gender == 'f':
        #print(gender)
        nameOfFillFile = 'parameters\FEMALE_PLAYER_LIST.csv'
        tempTornementFile = worldFile + 'playerStates\TEMP_TORNEMENT_FEMALE.csv'
        genderMod = 1
    elif gender == 'm':
        nameOfFillFile = 'parameters\MALE_PLAYER_LIST.csv'
        tempTornementFile = worldFile + 'playerStates\TEMP_TORNEMENT_MALE.csv'
        genderMod = 0

    with open(tempTornementFile, "r") as pointsFile:
        thesePlayers = csv.reader(pointsFile, delimiter=',', quotechar='|')
        for players in thesePlayers:
            tempDataList.append(players)

    #Add points from round one. Then, add points if player not advancing, remove points if player advancing. Simply assign points to winner.
    for i in range(len(tempDataList)):
        for j in range(len(currentWinners)):
            #Score mod from part B. score margin multiplier
            if currentWinnersScoreMargin[j] == 1:
                scoreMod = 1
            else:
                scoreMod = genderMod + currentWinnersScoreMargin[j] - 0.5
            #Round 1
            if roundNumber == '1':
                if currentWinners[j] == tempDataList[i][0]:
                    tempScore = float(tempDataList[i][1])
                    tempDataList[i].insert(1, tempScore + (float(rankPoints) * scoreMod))
                    tempDataList[i].insert(2, scoreMod)
                    tempDataList[i].pop(3)
            #Round 5
            elif roundNumber == '5':
                if currentWinners[j] == tempDataList[i][0]:
                    tempScore = float(tempDataList[i][1])
                    tempDataList[i].insert(1, (float(rankPoints) * scoreMod))
                    tempDataList[i].insert(2, scoreMod)
            #Round 2-4
            else:
                if currentWinners[j] == tempDataList[i][0]:#CHANGED FROM ORIGINAL: tempPlayerListWinners[j] == tempDataList[i][0]
                    tempScore = float(tempDataList[i][1])
                    tempDataList[i].insert(1, float(rankPoints) * scoreMod)
                    tempDataList[i].insert(2, scoreMod)

    #Save points back into file
    with open(tempTornementFile, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(tempDataList)):
            writePoints.writerow(tempDataList[players])

    global copyForSortRankForRound
    copyForSortRankForRound = tempDataList
    tennisTools.copyForRankPointDifficulty = tempDataList


#Clears temporary in tornement save file
def clearTempFileForPastTornement(gender):
    worldFile = worldSpecific.sendPath
    tempData = []
    zero = 0

    #Select gender of files
    if gender == 'f':
        x = worldFile + 'playerStates\TEMP_TORNEMENT_FEMALE.csv'
        a = 'parameters\FEMALE_PLAYER_LIST.csv'
    elif gender == 'm':
        x = worldFile + 'playerStates\TEMP_TORNEMENT_MALE.csv'
        a = 'parameters\MALE_PLAYER_LIST.csv'

    #Store player list
    with open(a, "r") as pointsFile:
        femalePlayers = csv.reader(pointsFile, delimiter=',', quotechar='|')
        for players in femalePlayers:
            tempData.append(players)


    #Restore file to default. List of players with score of zero
    with open(x, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(tempData)):
            writePoints.writerow(tempData[players] + [zero])

#Reset overall season points at the end of each season. Only seeding to be brought over
def resetOverAllAtEndOfSeason():
    worldFile = worldSpecific.sendPath
    MplainListOfPlayers = []
    FplainListOfPlayers = []
    zero = 0


    FoverallPoints = worldFile + 'playerStates\OVERALL_POINTS_WOMEN.csv'
    FprizeMoney =  worldFile + 'playerStates\PRIZE_TOTAL_FEMALE.csv'
    FplayersFile = 'parameters\FEMALE_PLAYER_LIST.csv'

    MoverallPoints = worldFile + 'playerStates\OVERALL_POINTS_MEN.csv'
    MprizeMoney =  worldFile + 'playerStates\PRIZE_TOTAL_MALE.csv'
    MplayersFile = 'parameters\MALE_PLAYER_LIST.csv'

    #Copy in plain list of players
    with open(FplayersFile, "r") as FseedyFile:
        thesePlayers = csv.reader(FseedyFile, delimiter=',', quotechar='|')
        for players in thesePlayers:
            FplainListOfPlayers.append(players)

    with open(MplayersFile, "r") as MseedyFile:
        thesePlayers = csv.reader(MseedyFile, delimiter=',', quotechar='|')
        for players in thesePlayers:
            MplainListOfPlayers.append(players)


    #OverWrite overall pointsFile
    with open(FoverallPoints, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(FplainListOfPlayers)):
            writePoints.writerow(FplainListOfPlayers[players] + [zero])

    #OverWrite overall pointsFile
    with open(MoverallPoints, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(MplainListOfPlayers)):
            writePoints.writerow(MplainListOfPlayers[players] + [zero])

    #OverWrite overall prizemoney
    with open(FprizeMoney, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(FplainListOfPlayers)):
            writePoints.writerow(FplainListOfPlayers[players] + [zero])

    #OverWrite overall prizemoney
    with open(MprizeMoney, "w", newline='') as pointsFile:
        writePoints = csv.writer(pointsFile, delimiter =',', quotechar='|' )
        for players in range(len(MplainListOfPlayers)):
            writePoints.writerow(MplainListOfPlayers[players] + [zero])
