import requests
import lxml
import time
import math
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from formatUtil import getZip

def truecar(make, model, city, state):
    # Use page 1 to get last number of pages
    link = "https://www.truecar.com/used-cars-for-sale/listings/" + make + "/" + model + "/location-" + city + "-" + state + "/?page=1&sort[]=best_match"
    site = requests.get(link)
    soup = BeautifulSoup(site.text, "lxml")
    alphaSoup = soup.find_all(class_="page-link")
    nums = list()
    num = int()

    for link in alphaSoup:
        if len(str(link.contents[0])) <= 2:
            nums.append(link.contents[0])
    try:
        num = int(nums[-1])
    except TypeError:
        print("banana")
    except IndexError:
        return [link]

    # Use number of pages to create a list of links for every page number
    linkList = list()
    for number in range(num):
        linkList.append("https://www.truecar.com/used-cars-for-sale/listings/" + make + "/" + model + "/location-" + city + "-" + state + "/?page=" + str(num) + "&sort[]=best_match")
        num -= 1
    print("Done Creating URL For TrueCar!")
    return linkList

def cargurus(make, model, city, state):
    # Starts by instantiating the Selenium web driver
    driver = webdriver.Firefox()
    # Opens the cargurus homepage with the driver
    driver.get("https://www.cargurus.com/")
    # Gets a random ZIP code with city and state because CarGurus only accepts ZIP for location
    zipCode = getZip(city, state)
    # Creates a dictionary with the arguments needed in JS
    argDict = {'make': make, 'model': model, 'zip': zipCode}
    # Opens the JavaScript file to grab the text
    jsScript = ''
    with open('js/cargurusLinker.js') as jsFile:
        jsScript = jsFile.read()
    # Injects the script into the carGurus page with the given arguments
    driver.execute_script(jsScript, argDict)
    # Waits 2 seconds before grabbing the URL
    time.sleep(2)
    url = driver.current_url
    # Grabs the max page count off the page
    maxPagesSpan = driver.find_element_by_class_name("_5kJMfL")
    maxPagesText = maxPagesSpan.text
    maxPagesSplit = maxPagesText.split(" ")
    maxPagesCount = int(maxPagesSplit[len(maxPagesSplit) - 1])
    # Closes the webdriver
    driver.close()
    # Generates a list of all the links to different result pages
    linkList = [url]
    for num in range(2, maxPagesCount + 1):
        linkList.append(url + "#resultsPage=" + str(num))
    # Finally returns the list
    print("Done Creating URL For CarGurus!")
    return linkList

def edmunds(make, model, city, state):
    # Gets a ZIP code with city
    zipCode = getZip(city, state)
    # Creates a url to the API with the make, model, and zip 
    url = "https://www.edmunds.com/gateway/api/purchasefunnel/v1/srp/inventory?inventoryType=used%2Ccpo&make=" + make + "&model=" + "-".join(model.split(" ")) + "&zip=" + zipCode + "&pageSize=24"
    # Makes a request to the API to grab pageSize
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    request = requests.get(url, headers=headers)
    # Uses beautifulsoup to digest the source
    soup = BeautifulSoup(request.text, "lxml")
    # Grabs the max pages element out of the json data
    jsonP = soup.contents[0].find("p")
    maxPages = json.loads(jsonP.contents[0])['inventories']['totalPages']
    # Creates the link list for the different pages
    linkList = [url]
    for num in range(2, maxPages + 1):
        linkList.append(url + "&pageNum=" + str(num))
    # Returns the list for the scraper
    print("Done Creating URL For Edmunds!")
    return linkList

def autotrader(make, model, city, state):
    # Gets a ZIP code with city
    zipCode = getZip(city, state)
    # Creates the URL
    url = "https://www.kbb.com/cars-for-sale/all/" + make + "/" + model + "/" + city + "-" + state + "-" + zipCode + "?dma=&searchRadius=100&location=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25"
    # Grabs the max record count off the page
    # AutoTrader does paging in the URL through record limiting and not pages
    siteText = requests.get(url).text
    soup = BeautifulSoup(siteText, "lxml")
    maxRecordSpan = soup.find(class_="results-text-container")
    maxRecordText = maxRecordSpan.contents[0].replace("+", "").replace(",", "")
    maxRecordSplit = maxRecordText.split(" ")
    maxRecordCount = int(maxRecordSplit[2])
    # Generates a list of all the links to different result pages
    linkList = [url]
    for num in range(25, maxRecordCount, 25):
        linkList.append(url + "&firstRecord=" + str(num))
    # Finally returns the list
    print("Done Creating URL For AutoTrader!")
    return linkList