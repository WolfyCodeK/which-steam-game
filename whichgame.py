from random import randrange
from time import sleep
from bs4 import BeautifulSoup
import requests
import re
import os

class GameChooser():
    # unicode values to be converted
    unicodeValues = {
    "\\u2122" : "™",
    "\\u00ae" : "®",
    }
    
    # thread sleep length
    pauseLength = 0.75
    
    def __init__(self) -> None:
        self.username = ""
    
    # runs all functions needed to find games
    def find_games(self):
        self.__set_username()
        self.__games_options()
        self.__delete_files()

    # get url of steam users games
    def __get_url(self, username):
        url = "https://steamcommunity.com/id/" + username + "/games/?tab=all"
        return url

    # Delete files at the end
    def __delete_files(self):
        if os.path.exists("jsData.txt"):
            os.remove("jsData.txt")

    def __set_username(self):
        validUserName = False
        # while the username entered has a corresponding profile
        while validUserName == False: 
            self.username = input("> () Steam account username -> ")

            # scrape data
            allData = self.__collect_all_data(self.__get_url(self.username))
            jsData = self.__collect_js_data(allData)

            # store that data
            filename = "jsData.txt"
            self.__write_data(jsData, "jsData.txt")

            # if the js data is empty, the username is invalid
            if self.__is_file_empty(filename) == True:
                print("> ({}) Invalid username".format(self.username))
                sleep(self.pauseLength)
                print("> ({}) Please try again".format(self.username))
            else:
                validUserName = True

    def __print_games(self, gamesList, limit):
        selectedGames = [gamesList[randrange(0,limit)], gamesList[randrange(0,limit)], gamesList[randrange(0,limit)]]
        
        print("> ({}) Selected Games: |{}| |{}| |{}|".format(self.username, selectedGames[0], selectedGames[1], selectedGames[2]))
        self.__write_data(selectedGames, "chosen-games.txt", True)

    # list out game options given some user options
    def __games_options(self):
        # store games list
        gamesList = self.__collect_games_list("jsData.txt")
        
        # get number of games in list
        numOfgames = len(gamesList) - 1

        # if there is at least 1 game in the users steam library
        if numOfgames >= 0:
            validOption = False
            # loop until wholeLibraryOption is a valid option
            while validOption == False:
                wholeLibraryOption = input("> ({}) Choose from whole library (y/n) -> ".format(self.username))
                sleep(self.pauseLength)
                
                if wholeLibraryOption == "y":
                    # randomly select 3 games for the user to play from whole library
                    self.__print_games(gamesList, numOfgames)
                    
                    validOption = True
                elif wholeLibraryOption == "n":
                    limitedSelection = 0
                    
                    # check limited selection is within range
                    while limitedSelection < 3 or limitedSelection > numOfgames:
                        limitedSelection = int(input("> ({}) Library selection size from (3-{}) -> ".format(self.username, numOfgames)))
                        
                    sleep(self.pauseLength)
                    
                    # randomly select 3 games for the user to play from selection
                    self.__print_games(gamesList, limitedSelection)
                    
                    validOption = True
                else:
                    validOption = False
        else:
            print("> ({}) No games were found".format(self.username))
            sleep(self.pauseLength)

    # check if file is empty
    def __is_file_empty(self, filename):
        file = open(filename, "r", encoding="utf-8")
        data = file.read()
        if (data.startswith("[]")):
            return True
        else: 
            return False
        
    # scrape all data from a url
    def __collect_all_data(self, url):
        result = requests.get(url)
        data = result.text
        
        return data

    # filter only javascript from a textfile
    def __collect_js_data(self, data):
        htmlData = BeautifulSoup(data, "html.parser")
        jsData = str(htmlData.find_all(attrs={"language" : "javascript"}))
        
        return jsData

    # write data to a text file
    def __write_data(self, data, filename):
        file = open(filename, "w", encoding="utf-8")
        
        # write either an entire string or a list of strings to a text file
        if type(data) == str:
            file.write(data)
        elif type(data) == list:
            for elem in data:
                for key in self.unicodeValues:
                    elem = elem.replace(key, self.unicodeValues[key])
                file.write(elem)
                file.write("\n")
                
        file.close()

    # create a list of games
    def __collect_games_list(self, filename):
        file = open(filename, "r")
        data = file.read()
        
        # filter out names of games
        games = re.findall(r'"name\":\"(.*?)\"', data)
        
        return games