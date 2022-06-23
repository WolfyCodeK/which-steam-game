from random import randrange
from time import sleep
from bs4 import BeautifulSoup
import requests
import re

"""  
TO-DO
1. find out why only logged in steam profile can be viewed
2. find other codes to be replaced "\u2122"
"""

unicodeValues = {
    "\\u2122" : "™",
    "\\u00ae" : "®",
}

pauseLength = 0.75

# get url of steam users games
def get_url():
    username = input("Username: ")
    print("")
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

while validUserName == False:
    allData = collect_all_data(get_url())
    jsData = collect_js_data(allData)
    
    filename = "jsData.txt"
    write_data(jsData, "jsData.txt")
    
    if is_file_empty(filename) == True:
        print("> Invalid username")
        sleep(pauseLength)
        print("> Please try again", end="\n")
    else:
        validUserName = True
    
gamesList = collect_games_list("jsData.txt")
write_data(gamesList, "gamesList.txt")

numOfgames = len(gamesList) - 1

input("> Selected Games: {}, {}, {}".format(gamesList[randrange(0,numOfgames)], gamesList[randrange(0,numOfgames)], gamesList[randrange(0,numOfgames)]))

print("> END OF PROGRAM")
sleep(pauseLength)