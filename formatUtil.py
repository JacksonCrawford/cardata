# Utility functions for formatting scraped car data
from more_itertools import unique_everseen
from pathlib import Path

def createYMMString(year, make, model):
    # @param year - an integer for the year of the car (ex. 2021)
    # @param make - a string saying which company made the car (ex. "Porsche")
    # @param model - a string saying what model the car is (ex. "Macan")
    if year and make and model:
        return str(year) + " " + make + " " + model
    else:
        return "Something Is Definitely Wrong! D:"

def createLocationString(distance, city):
    # @param distance - an integer of the distance to the car (in miles, ex. 48.93)
    # @param city - a string of the city where the car is located (ex. "Charlotte")
    if distance and city:
        return str(round(distance)).replace(",", "") + " mi - " + city
    else:
        return "Not Listed"

def createColorString(exteriorColor, interiorColor):
    # @param exteriorColor - a string of a normalized exterior color (ex. "White")
    # @param interiorColor - a string of a normalized interior color (ex. "Black")
    if exteriorColor and interiorColor:
        # Normalizes the colors to have the first letter capitalized and the rest lowercase
        # Ex. Turns "WHITE" into "White"
        normalizedExterior = exteriorColor[0].upper() + exteriorColor[1:].lower()
        normalizedInterior = interiorColor[0].upper() + interiorColor[1:].lower()
        # Returns the concatenated string format
        return normalizedExterior + " exterior " + normalizedInterior + " interior"
    else:
        return "Not Listed"

def getZip(city, state):
    import requests
    import json
    # @param city - a string of the city where the car is located (ex. "Charlotte")
    # @param state - a string of the state code where the car is located (ex. "NC")
    # Starts by making a request to the Zippopotamus API
    request = requests.get("http://api.zippopotam.us/us/" + state + "/" + city)
    # Parses the returned request as a json
    jsonResults = json.loads(request.text)
    # Returns the first result in the list
    if len(jsonResults['places']) > 0:
        return jsonResults['places'][0]['post code']
    else:
        print("Something went wrong while retrieving ZIP Code for " + city + ", " + state + "!")
        return "0"

def addHeaders(fileName):
    with open(fileName, "a") as headFile:
        headFile.write("year,price,mileage\n")
        headFile.close()

def removeDupe(fileName):
    master = None
    with open(fileName, "r") as infile:
        master = infile.read().split("\n")
        infile.close()
    with open(fileName, "w") as outfile:
        outfile.writelines("\n".join(list(unique_everseen(master))))
        outfile.close()
    print("Done Duplicate Checking master.csv!")

def fileWipe(fileName):
    # @param fileName - a string with the path and filename of a file (ex. "output/truecar.csv")
    # Wipes a file
    with open(fileName, "w") as f:
        f.close()

def firstLetterCapitals(string):
    # @param string - input string that will have first letter capitalized
    splitString = string.split(" ")
    capitalizedSplitString = []
    for split in splitString:
        capitalizedSplitString.append(split[0].upper() + split[1:].lower())
    return " ".join(capitalizedSplitString)
