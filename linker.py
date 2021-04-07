import requests
import lxml
import time
import math
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from formatUtil import firstLetterCapitals, getZip, firstLetterCapitals

# Requests header User Agent
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

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
    # Finds the fields for make, model, and zip
    makeField = Select(driver.find_element_by_id("carPickerUsed_makerSelect"))
    modelField = Select(driver.find_element_by_id("carPickerUsed_modelSelect"))
    zipField = driver.find_element_by_id("dealFinderZipUsedId_dealFinderForm")
    # Selects the correct option for make and model
    makeField.select_by_visible_text(firstLetterCapitals(make))
    modelField.select_by_visible_text(firstLetterCapitals(model))
    # Clears the zip field then inputs the text
    zipField.send_keys(Keys.CONTROL + "a")
    zipField.send_keys(Keys.DELETE)
    zipField.send_keys(zipCode)
    # Submits the form to get to the next page
    submitButton = driver.find_element_by_id("dealFinderForm_0")
    submitButton.click()
    # Waits 2 seconds and grabs the final URL
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
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'referer': 'https://www.edmunds.com/'}
    url = "https://www.edmunds.com/gateway/api/purchasefunnel/v1/srp/inventory?inventoryType=used%2Ccpo&make=" + make + "&model=" + "-".join(model.split(" ")) + "&zip=" + zipCode + "&pageSize=24"
    # Makes a request to the API to grab pageSize
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

def carsdotcom(make, model, city, state):
    # Starts by instantiating the Selenium web driver
    driver = webdriver.Firefox()
    # Opens the cargurus homepage with the driver
    driver.get("https://www.cars.com/")
    # Gets a random ZIP code with city and state because CarGurus only accepts ZIP for location
    zipCode = getZip(city, state)
    # Finds the fields for stock type, make, model, and zip
    stockTypeField = Select(driver.find_element_by_name("stockType"))
    makeField = Select(driver.find_element_by_name("makeId"))
    modelField = Select(driver.find_element_by_name("modelId"))
    zipField = driver.find_element_by_name("zip")
    # Sets the value of each select field
    stockTypeField.select_by_visible_text("Used Cars")
    makeField.select_by_visible_text(firstLetterCapitals(make))
    modelField.select_by_visible_text(firstLetterCapitals(model))
    # Wipes the zipField and puts in our zip
    zipField.send_keys(Keys.CONTROL + "a")
    zipField.send_keys(Keys.DELETE)
    zipField.send_keys(zipCode)
    # Sends an enter keypress to the zipField to submit the form
    zipField.send_keys(Keys.ENTER)
    # Waits 2 seconds before grabbing the URL
    time.sleep(2)
    url = driver.current_url
    driver.close()
    # Parses the make and model codes from the URL
    modelCodeParameter = "mdId="
    makeCodeParameter = "mkId="
    modelCodeLocation = url.find(modelCodeParameter) + len(modelCodeParameter) 
    makeCodeLocation = url.find(makeCodeParameter) + len(makeCodeParameter) 
    modelCode = url[modelCodeLocation:url.find("&", modelCodeLocation)]
    makeCode = url[makeCodeLocation:url.find("&", makeCodeLocation)]
    # Makes a request to the API with the grabbed make and model code 
    apiUrl = "https://www.cars.com/for-sale/listings/?perPage=100&rd=50&returnRecs=false&searchSource=PAGINATION&sort=relevance&zc=85044&mdId=" + modelCode + "&mkId=" + makeCode
    # Grabs the max page count off of the json
    request = requests.get(apiUrl, headers=headers)
    dataDict = json.loads(request.text)
    pageCount = dataDict["json"]["pagination"]["numberOfPages"]
    # Generates a list of all the links to different result pages
    linkList = [apiUrl]
    for num in range(2, pageCount + 1):
        linkList.append(apiUrl + "&page=" + str(num))
    # Finally returns the list
    print("Done Creating URL For Cars.com!")
    return linkList
