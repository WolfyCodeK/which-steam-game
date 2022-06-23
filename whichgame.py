from random import randrange
from time import sleep
from bs4 import BeautifulSoup
import requests
import re

"""  
TO-DO
1. find out why only logged in steam profile can be viewed
"""

# unicode values to be converted
unicodeValues = {
    "\\u2122" : "™",
    "\\u00ae" : "®",
}

# thread sleep length
pauseLength = 0.75

# get url of steam users games
def get_url(username):
    url = "https://steamcommunity.com/id/" + username + "/games/?tab=all"
    return url

# check if file is empty
def is_file_empty(filename):
    file = open(filename, "r", encoding="utf-8")
    data = file.read()
    if (data.startswith("[]")):
        return True
    else: 
        return False
    
# scrape all data from a url
def collect_all_data(url):
    result = requests.get(url)
    data = result.text
    
    return data

# filter only javascript from a textfile
def collect_js_data(data):
    htmlData = BeautifulSoup(data, "html.parser")
    jsData = str(htmlData.find_all(attrs={"language" : "javascript"}))
    
    return jsData

# write data to a text file
def write_data(data, filename):
    file = open(filename, "w", encoding="utf-8")
    
    # write either an entire string or a list of strings to a text file
    if type(data) == str:
        file.write(data)
    elif type(data) == list:
        for elem in data:
            for key in unicodeValues:
                elem = elem.replace(key, unicodeValues[key])
            file.write(elem)
            file.write("\n")
            
    file.close()

# create a list of games
def collect_games_list(filename):
    file = open(filename, "r")
    data = file.read()
    
    # filter out names of games
    games = re.findall(r'"name\":\"(.*?)\"', data)
    
    return games


#---Main---#
validUserName = False

# while the username entered has a corresponding profile
while validUserName == False: 
    username = input("Username: ")
    print("")
    
    # scrape data
    allData = collect_all_data(get_url(username))
    jsData = collect_js_data(allData)
    
    # store that data
    filename = "jsData.txt"
    write_data(jsData, "jsData.txt")
    
    # if the js data is empty, the username is invalid
    if is_file_empty(filename) == True:
        print("> ({}) Invalid username".format(username))
        sleep(pauseLength)
        print("> ({}) Please try again\n".format(username))
    else:
        validUserName = True

# store games list
gamesList = collect_games_list("jsData.txt")
write_data(gamesList, "gamesList.txt")

numOfgames = len(gamesList) - 1

# if there is at least 1 game in the users steam library
if numOfgames >= 0:
    validOption = False
    # loop until wholeLibraryOption is a valid option
    while validOption == False:
        wholeLibraryOption = input("> ({}) Choose from whole library? y/n\n> ".format(username))
        sleep(pauseLength)
        
        if wholeLibraryOption == "y":
            # randomly select 3 games for the user to play from whole library
            print("> ({}) Selected Games: {}, {}, {}".format(username, gamesList[randrange(0,numOfgames)], gamesList[randrange(0,numOfgames)], gamesList[randrange(0,numOfgames)]))
           
            validOption = True
        elif wholeLibraryOption == "n":
            limitedSelection = 0
            while limitedSelection < 3 or limitedSelection > numOfgames:
                limitedSelection = int(input("> ({}) Starting from highest playtime, how many games would you like to choose from (3-{})? \n> ".format(username, numOfgames)))
            sleep(pauseLength)
            # randomly select 3 games for the user to play from selection
            print("> ({}) Selected Games: {}, {}, {}".format(username, gamesList[randrange(0,limitedSelection)], gamesList[randrange(0,limitedSelection)], gamesList[randrange(0,limitedSelection)])) 
            
            validOption = True
        else:
            validOption = False
else:
    print("> ({}) No games were found".format(username))
    sleep(pauseLength)

input("--- END OF PROGRAM ---")