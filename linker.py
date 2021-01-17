import requests
import lxml
import time
from bs4 import BeautifulSoup
from selenium import webdriver
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

    return linkList

def cargurus(make, model, city, state):
    # Starts by instantiating the Selenium web driver
    driver = webdriver.Firefox()
    # Opens the cargurus homepage with the driver
    driver.get('https://www.cargurus.com/')
    # Gets a random ZIP code with city and state because CarGurus only accepts ZIP for location
    zipCode = getZip(city, state) 
    # Creates a dictionary with the arguments needed in JS
    argDict = {'make': make, 'model': model, 'zip': zipCode}
    # Opens the JavaScript file to grab the text
    jsScript = ''
    with open('js/cargurusLinker.js') as jsFile:
        jsScript = jsFile.read()
    # Injects the script into the carGurus page with the given arguments, JS script will return generated link
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
    linkList = []
    for num in range(2, maxPagesCount + 1):
        linkList.append(url + "#resultsPage=" + str(num))
    # Finally returns the list
    return linkList
