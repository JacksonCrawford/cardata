import requests
import json
import formatUtil
from bs4 import BeautifulSoup
from config import CarConfig
import linker

def scraper(fileName):
    # Creates a config to grab info for the linker
    config = CarConfig()
    # Opens the CSV file for data storage
    # Uses w+ mode; will create the csv file if it doesn't exist
    file = open(fileName, "a")
    for link in linker.cargurus(config.getMake(), config.getModel(), config.getCity(), config.getState()):
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
                        # print(csvString)
                        file.write(csvString + "\n")
    # Closes the csv file
    file.close()
    print("Done Scraping CarGurus!")


if __name__ == '__main__':
    # Wipes the CSV file
    formatUtil.fileWipe("output/cargurus.csv")
    # Starts the scraper
    scraper("output/cargurus.csv")
