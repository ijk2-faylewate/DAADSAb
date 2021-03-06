import tennisTools
import ranking
import prizeMoney
import manualInput
import sys
import sortLists
import menuFunctions
import worldSpecific
import seasonSpecific
import statistics

#seasonSpecific.setSeeds('f', None, None)

#Choose/create world file
worldSpecific.fileSelect(menuFunctions.createOrOpenWorld())
worldFile = worldSpecific.sendPath
print(worldFile)
#Set saved data files to default(Does not delete results files)
menuFunctions.dataWipe()
#########################
#START MAIN PROGRAM LOOP#
#########################
while True:
    #TODO Menu option: Ask if user wants to start new first season, or continue
    #With next season in series, (?)
    #TODO Functionality: check and update seedList
    seasonSpecific.checkAndInit()
    seasonNumber = 'SEASON_' + str(seasonSpecific.seasonNumber) + '_'

    #Populate list of Male Players
    listOfMalePlayers = []
    tennisTools.fillPlayerList('parameters\MALE_PLAYER_LIST.csv', listOfMalePlayers)

    #Populate list of female players
    listOfFemalePlayers = []
    tennisTools.fillPlayerList('parameters\FEMALE_PLAYER_LIST.csv', listOfFemalePlayers)

    #TODO Logic: If season started but not finished, do not allow user to re-run tornemnet.
    #However, this may need to happen after gender selection. Possible to swap in order?

    #Gender select
    selectGender= menuFunctions.genderSelector()

    #Tornement select
    tornement = menuFunctions.tornementSelector(selectGender)

    #Simple string to complete nameOfFile
    fileType = '.csv'

    #Check if previous tornement of this type ended properly
    checkPrevious = tennisTools.checkIfPreviousComplete(tornement, selectGender)

    #IF PREVIOUS TORNEMENT OF THIS TYPE COMPLETED, RUN AS NORMAL
    if checkPrevious == 'TRUE':
        #Manual input option
        manualSelect = menuFunctions.manualSelector()
        #Initialize round for start of tornement
        playRound = 0
        #Play next round
        playRound = menuFunctions.playNextRound(playRound)
        print('Round: ',  playRound)

        #Determine list of players to use
        if selectGender == 'f':
            gender = '_WOMEN'
            if manualSelect == 'n':
                listSelect = listOfFemalePlayers
        elif selectGender == 'm':
            gender = '_MEN'
            if manualSelect == 'n':
                listSelect = listOfMalePlayers

        #Recieve manual input if requested, else ignore
        if manualSelect == 'y':
            listSelect = manualInput.userInputStack(selectGender, str(playRound))
        else:
            pass

        #Name of Round File to be generated
        paramLocation = worldFile #'parameters\\'
        nameOfFile = paramLocation + seasonNumber + tornement + str(playRound) + gender + fileType
        print(nameOfFile)

        ######################################
        #START ROUND 1 (INITIALIZE TORNEMENT)#
        ######################################

        #Determine seeds
        seasonSpecific.isSeed(tornement,selectGender,playRound)

        #Set fixtures, generate scores, write to file.
        if manualSelect == 'n':
            tennisTools.setFixtures(nameOfFile,listSelect, selectGender, int(playRound))
        else:
            tennisTools.setFixturesFromManual(nameOfFile,listSelect, selectGender)

        #seasonSpecific.currentSeeded.clear()
        #Determine winners by reading file created in previous step. Display Results
        #print(gender + selectGender + '1')
        tennisTools.runRoundNew(nameOfFile,selectGender)


        seasonSpecific.setSeeds(selectGender,tornement)#CHANGED: #Needs uncommenting, when structure inplace to keep in step with seasons

        #Update Ranking points, both per round and overall. Add statistics.
        statistics.playerStatistics(selectGender)#CHANGED:New bit for stats
        ranking.updatePointsCurrentTornement(tornement, str(playRound), selectGender)
        ranking.updateRankPoints(tornement, str(playRound), selectGender)

        #Determine money owed to each player
        prizeMoney.calculatePrizeMoney(tornement, str(playRound), selectGender)

        #Record tornement as complete, or not.
        tennisTools.writePreviousComplete(tornement, selectGender, playRound)

        #Enable sorted lists
        cantSee = False
        #print('From fixtures')
        #print(seasonSpecific.currentSeeded)
    #IF PREVIOUS ROUND OF THIS TORNEMENT TYPE DID NOT FINISH, RE-RUN ROUND PRIOR TO SHUTDOWN
    elif checkPrevious == 'FALSE':
        if selectGender == 'f':
            gender = '_WOMEN'
        elif selectGender == 'm':
            gender = '_MEN'
        #Get number of round to restart from (i.e. round played just before tornement finished prematurely)
        playRound = tennisTools.restartRound

        #Name of previous round
        paramLocation = worldFile#'parameters\\'
        nameOfFile = paramLocation + seasonNumber + tornement + str(playRound) + gender + fileType
        #Re-run round, but don't update anything as those points already added
        #print(gender + selectGender + '2')
        tennisTools.runRoundNew(nameOfFile,selectGender)

        #Don't display option to view sorted list if re-running un-finished tornement
        cantSee = True
        manualSelect = 'n'

    #end check#

    ################################
    #LOOP THROUGH SUBSEQUENT ROUNDS#
    ################################

    while int(playRound) != 5:
        if cantSee == False:
            #check players' earnings
            menuFunctions.checkPrizeMoney(selectGender)
            #Check leader board for round
            menuFunctions.checkPointsFromRound()
            #check overall leader bourd
            menuFunctions.checkOverallRankPoints()
            #stats
            menuFunctions.viewPlayerStatsTornement()
        else:
            pass

        #Enable sorted lists
        cantSee = False


        #Select manual option
        manualSelect = menuFunctions.manualSelector()

        #Confirm play next round and add players to list for next round
        if manualSelect == 'y':
            playRound = menuFunctions.playNextRound(playRound)
            listSelect = manualInput.userInputStack(selectGender, str(playRound))
        else:
            playRound = menuFunctions.playNextRound(playRound)
            #if int(seasonSpecific.seasonNumber) == 1:
            listSelect = tennisTools.currentWinners
            #elif int(seasonSpecific.seasonNumber) > 1:
             #   if selectGender == 'f':
              #      listSelect = listOfFemalePlayers
               # elif selectGender == 'm':
                #    listSelect = listOfMalePlayers

        #Determine seeds
        seasonSpecific.isSeed(tornement,selectGender,playRound)
        #Display round number
        print('Round: ', playRound)

        #select file depending on round
        nameOfFile = paramLocation + seasonNumber + tornement + str(playRound) + gender + fileType
        print(nameOfFile)

        #Set fixtures, generate scores, write to file.
        if manualSelect == 'y':
            tennisTools.setFixturesFromManual(nameOfFile,listSelect, selectGender)
        else:
            tennisTools.setFixtures(nameOfFile,listSelect, selectGender, int(playRound))

        #seasonSpecific.currentSeeded.clear()

        #Clear curent winners list, so a new list of winners can be made from this round
        tennisTools.currentWinners.clear()
        tennisTools.currentWinnersScoreMargin.clear()
        tennisTools.currentLosers.clear()

        #Determine winners by reading file created in previous step. Display Results
        tennisTools.runRoundNew(nameOfFile,selectGender)

        #seasonSpecific.isSeed(tornement,selectGender,playRound)
        seasonSpecific.setSeeds(selectGender,tornement)#CHANGED:

        #Update Ranking points, both per round and overall, Add statistics.
        statistics.playerStatistics(selectGender)#CHANGED:New bit for stats
        ranking.updatePointsCurrentTornement(tornement, str(playRound), selectGender)
        ranking.updateRankPoints(tornement, str(playRound), selectGender)

        #Determine money owed to each player
        prizeMoney.calculatePrizeMoney(tornement, str(playRound), selectGender)

        #Record tornement as complete, or not.
        tennisTools.writePreviousComplete(tornement, selectGender, str(playRound))

    #View overall stats for overall season
    #menuFunctions.viewPlayerStatsSeason()
    #Really Tracks Whether or not a tornemnet has been played, and tracks which season Currently being played
    #seasonSpecific.setTornementPlayed(tornement,selectGender,str(playRound))

    #Clear temporary points file, as tornement finished
    ranking.clearTempFileForPastTornement(selectGender)

    #Commit Prize money to file
    prizeMoney.commitPrizeMoney(selectGender)

    #Clear temporary prize money file, as tornement finished
    prizeMoney.clearTemporaryRoundFile(selectGender)

    #Empty current lists, avoid spill into next tornement
    tennisTools.currentWinners.clear()
    tennisTools.currentWinnersScoreMargin.clear()
    tennisTools.currentLosers.clear()

    #check players' earnings
    menuFunctions.checkPrizeMoney(selectGender)
    #Check leader board for round
    menuFunctions.checkPointsFromRound()
    #check overall leader bourd
    menuFunctions.checkOverallRankPoints()
    #stats
    menuFunctions.viewPlayerStatsTornement()

    #UpdateOverall stats, clear temp
    statistics.updateSeasonStatsClearTemp(selectGender)

    #View overall stats for overall season
    menuFunctions.viewPlayerStatsSeason()
    #Really Tracks Whether or not a tornemnet has been played, and tracks which season Currently being played
    seasonSpecific.setTornementPlayed(tornement,selectGender,str(playRound))

    #Exit System?
    #exitSystem = input('Exit Program: Y/N').upper()
    exitSystem = menuFunctions.exitSelector()
    if exitSystem == 'Y':
        sys.exit(0)
    else:
        pass

#######################
#END MAIN PROGRAM LOOP#
#######################
