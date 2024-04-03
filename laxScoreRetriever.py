import requests
import sys
from datetime import datetime
from datetime import timedelta
import os

def generateResultsOutputFromJson(gamesJson):
    results = []
    for game in gamesJson:
        homeTeam = game["HostTeamName"]
        homeScore = game["HostScore"]
        awayTeam = game["AwayTeamName"]
        awayScore = game["AwayScore"]
        if homeTeam != None and homeScore != None and awayTeam != None and awayScore != None:
            gameString = formatGameResult(homeTeam, homeScore, awayTeam, awayScore)
            results.append(gameString)
    return results

def generateScheduleOutputFromJson(gamesJson):
    results = []
    for game in gamesJson:
        homeTeam = game["HostTeamName"]
        homeRecord = game["HostRecord"]
        awayTeam = game["AwayTeamName"]
        awayRecord = game["AwayRecord"]
        gameTime = game["ContestTime"]
        if homeTeam != None and homeRecord != None and awayTeam != None and awayRecord != None and gameTime != None:
            scheduleString = formatGameSchedule(homeTeam, homeRecord, awayTeam, awayRecord, gameTime)
            results.append(scheduleString)
    return results

def decrementDateOne(date):
    nowDate = datetime.strptime(date, "%Y-%m-%d")
    nextDay = nowDate - timedelta(days = 1)
    return nextDay.strftime("%Y-%m-%d")

def formatDate(date):
    monthDict = {"03": "March", "04": "April", "05": "May", "06": "June"}
    year = date.split("-")[0]
    month = monthDict[date.split("-")[1]]
    day = date.split("-")[2]
    return month + " " + day + ", " + year

def formatGameResult(homeTeam, homeScore, awayTeam, awayScore):
    if int(homeScore) > int(awayScore):
        return homeTeam + " " + homeScore + ", " + awayTeam + " " + awayScore + "\n"
    else:
        return awayTeam + " " + awayScore + ", " + homeTeam + " " + homeScore + "\n"

def formatGameSchedule(homeTeam, homeRecord, awayTeam, awayRecord, gameTime):
    return homeTeam + " (" + homeRecord + ") vs. " + awayTeam + " (" + awayRecord + "), " + gameTime + "\n"
def generateOutputHeader(gender, date):
    return "Completed Games\n" + formatDate(date) + "\nLacrosse (" + gender + ")\n"
def generateScheduleHeader(gender, date):
    return "Scheduled Games\n" + formatDate(date) + "\nLacrosse (" + gender + ")\n"

inputDate = datetime.now().strftime("%Y-%m-%d")
if (len(sys.argv) > 1):
    inputDate = sys.argv[1]

yesterday = decrementDateOne(inputDate)
today = inputDate

outputDir = os.getcwd() + "/" + inputDate
os.makedirs(outputDir)

# Output file names
boysOutputFile = "YesterdaysBoysLaxResults.txt"
girlsOutputFile = "YesterdaysGirlsLaxResults.txt"

boysScheduleFile = "TodaysBoysLaxSchedule.txt"
girlsScheduleFile = "TodaysGirlsLaxSchedule.txt"

# API urls
boysUrl = "https://my.mhsaa.com/DesktopModules/MHSAA-Endpoint/handlers/ContestWithParticipantDepotSearch.ashx?Method=ScoreCenterSearch&StartDate="+ yesterday + "&EndDate=" + yesterday + "&Sport=BBL&Level=V"
girlsUrl = "https://my.mhsaa.com/DesktopModules/MHSAA-Endpoint/handlers/ContestWithParticipantDepotSearch.ashx?Method=ScoreCenterSearch&StartDate="+ yesterday + "&EndDate=" + yesterday + "&Sport=GGL&Level=V"

# Get responses from APIs
boysResponse = requests.get(boysUrl)
girlsResponse = requests.get(girlsUrl)

# Convert response to json (basically python dictionary)
boysJson = boysResponse.json()
girlsJson = girlsResponse.json()

boysResults = generateResultsOutputFromJson(boysJson)
girlsResults = generateResultsOutputFromJson(girlsJson)


with open(outputDir + "/" + boysOutputFile, "w") as outfile:
    print("Outputing Yesterday's Boys Scores")
    outfile.write(generateOutputHeader("Boys", yesterday))

    for result in boysResults:
        outfile.write(result)

with open(outputDir + "/results/" + girlsOutputFile, "w") as outfile:
    print("Outputing Yesterday's Girls Scores")
    outfile.write(generateOutputHeader("Girls", yesterday))

    for result in girlsResults:
        outfile.write(result)

boysTomorrowUrl = "https://my.mhsaa.com/DesktopModules/MHSAA-Endpoint/handlers/ContestWithParticipantDepotSearch.ashx?Method=ScoreCenterSearch&StartDate="+ today + "&EndDate=" + today + "&Sport=BBL&Level=V"
girlsTomorrowUrl =  "https://my.mhsaa.com/DesktopModules/MHSAA-Endpoint/handlers/ContestWithParticipantDepotSearch.ashx?Method=ScoreCenterSearch&StartDate="+ today + "&EndDate=" + today + "&Sport=GGL&Level=V"

boysTomResponse = requests.get(boysTomorrowUrl)
girlsTomResponse = requests.get(girlsTomorrowUrl)

boysTomJson = boysTomResponse.json()
girlsTomJson = girlsTomResponse.json()

boysSchedule = generateScheduleOutputFromJson(boysTomJson)
girlsSchedule = generateScheduleOutputFromJson(girlsTomJson)

with open(outputDir + "/" + boysScheduleFile, "w") as outfile:
    print("Outputing Today's Boys Schedule")
    outfile.write(generateScheduleHeader("Boys", today))

    for sched in boysSchedule:
        outfile.write(sched)

with open(outputDir + "/" + girlsScheduleFile, "w") as outfile:
    print("Outputing Today's Girls Schedule")
    outfile.write(generateScheduleHeader("Girls", today))

    for sched in girlsSchedule:
        outfile.write(sched)