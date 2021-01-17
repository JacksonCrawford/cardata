import requests
from bs4 import BeautifulSoup
from config import CarConfig
import linker
import json
import formatUtil
import selenium.webdriver as webdriver

def truecar(url):
    # Opens the CSV file for data storage
    # Uses w+ mode; will create the csv file if it doesn't exist
    file = open("output/master.csv", "a")
    # Instantiates a Config object
    config = CarConfig()
    # Creates a GET request to the trueCar link in the config
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    creamySoup = soup.find(class_="row row-2 margin-bottom-3")
    # Finds all of the car info cards on the website
    cards = creamySoup.find_all(class_="card-content vehicle-card-body")
    # Loops through all of the info cards to gather data
    for card in cards:
        year = card.find(class_="vehicle-card-year font-size-1").contents[0]
        try:
            price = (card.find(class_="heading-3 margin-y-1 font-weight-bold")).contents[0].replace(",", "").replace("$", "")
        except AttributeError:
            price = "No Price"
        try:
            miles = str(card.find(class_="d-flex w-100 justify-content-between").contents[0])
            miles = miles[miles.find("</svg>") + 6:miles.find("</div>"):]
            miles = miles.replace("<!-- -->", "").replace(",", "").replace(" miles", "")
        except AttributeError:
            miles = "Not Listed"

        print(year + "," + price + "," + miles)

        data = year + "," + price + "," + miles
        file.write(data)
        file.write("\n")
    # Closes the CSV file after adding scraped data
    file.close()

def getSource(url):
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html

def cargurus(link):
    # Opens the CSV file for data storage
    # Uses w+ mode; will create the csv file if it doesn't exist
    file = open("output/master.csv", "a")
    # Creates a GET request to the carGurus link in the config
    site = requests.get(link)
    # Parses the website using lxml
    soup = BeautifulSoup(site.text, "lxml")
    # Grabs the script tags, we're looking for the "featuredListings" object somewhere in the React code
    scripts = soup.find_all("script")
    # Loops through the script tags looking for the featuredListings object
    for script in scripts:
        # Checks if the script tag has any contents
        if len(script.contents) <= 0:
            continue
        # Grabs the text from the script tag
        text = script.contents[0]
        # The script tag we're looking for is about 115,000
        # in size on a small query, so just filter out anything below a certain threshold
        if (len(text) > 50000):
            # Finds the location of the listings object
            startLocation = text.find('"featuredListings"') - 1
            # Checks if it actually exists in this script tag
            if startLocation:
                # Goes back one index to include the starting {
                # Finds the end of the listings object using the start of the next line
                endLocation = text.find("\n        window.__PREFLIGHT__", startLocation) - 1
                # Takes a substring to grab the entire object
                listingsText = text[startLocation: endLocation]
                # Converts from JSON text to a Python Dictionary
                listings = json.loads(listingsText)["listings"]
                # Starts putting data into CSV format
                for listing in listings:
                    # For Debug
                    # print(json.dumps(listing, sort_keys=True, indent=4))
                    # Grabs the year
                    year = listing["carYear"]
                    # Grabs the make
                    #make = listing["makeName"]
                    # Grabs the model
                    #model = listing["modelName"]
                    # Creates a Year Make Model string
                    #ymm = formatUtil.createYMMString(year, make, model)
                    # Grabs the price
                    price = listing["expectedPriceString"].replace(",", "").replace("$", "") or "No Price"
                    # Grabs the trim
                    # trim = listing["trimName"] or "Not Listed"
                    # Grabs the mileage
                    miles = (listing["mileageString"] + " miles").replace(",", "").replace(" miles", "") or "Not Listed"
                    # Grabs the location, have to append a couple entries to make this the same format as truecar
                    #location = formatUtil.createLocationString(listing["distance"], listing["sellerCity"].split(", ")[0])
                    # Grabs the color. Unfortunately CarGurus does not provide interior color.
                    #color = formatUtil.createColorString(listing["normalizedExteriorColor"], "Unknown")
                    # Puts the data into CSV format
                    #csvString = (ymm + ", " + price + ", " + trim + ", " + miles + ", " + location + ", " + color)
                    csvString = (str(year) + "," + price + "," + miles)
                    # Finally writes the CSV data to the file
                    print(csvString)
                    file.write(csvString + "\n")
    # Closes the csv file
    file.close()


def getSource(url):
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html

def edmunds(url):
    soup = BeautifulSoup(getSource(url), "lxml")
    edmundSoup = soup.find("usurp-card-list list-unstyled align-items-stretch row")

    outfile = open("output/edmunds.csv", "a")
    cards = soup.find_all(class_="d-flex mb-0_75 mb-md-1_5 col-12 col-md-6")
    for card in cards:
        year = str(card.find(class_="card-title size-16 text-primary-darker font-weight-bold d-block mb-0_5").contents[0])
        if "Certified" in year:
            year = year[10::]
        try:
            price = str((card.find(class_="display-price font-weight-bold text-gray-darker")).contents[0].replace(",", ""))
        except AttributeError:
            price = "No Price"
        try:
            miles = str(card.find(class_="col-6").contents[1])
            miles = miles.replace("class=\"size-14\">", "").replace("</span", "").replace(",", "").replace("<span ", "").replace(" miles>", "")
        except AttributeError:
            miles = "Not Listed"

        data = year[0:4:] + "," + price + "," + miles

        outfile.write(data)
        outfile.write("\n")
    outfile.close()

# Main Method
if __name__ == "__main__":
    # Creates a config to grab info for the linker
    config = CarConfig()
    # Wipes the file
    with open("output/master.csv", "w") as f:
        f.close()
    # Loops through all of the links provided by the linker and scrapes each page
    for link in linker.truecar(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        truecar(link)
    for link in linker.cargurus(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        cargurus(link)
    for link in linker.edmunds(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        edmunds(link)
