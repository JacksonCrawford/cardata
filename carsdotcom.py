import requests
import formatUtil
import linker
import json
from config import CarConfig
from pathlib import Path

def scraper(fileName):
    # Creates a CarConfig object for search criteria
    config = CarConfig()
    # Opens the CSV file for appending, will likely be wiped already
    file = open(fileName, "a")
    # Loops through each link provided by the linker and scrapes the site
    for link in linker.carsdotcom(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        # Makes a request to the edmunds site for the source code
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        site = requests.get(link, headers=headers)
        # Converts the data to JSON for easy digestion
        jsonData = json.loads(site.text)
        # Grabs car results from json
        results = jsonData["dtm"]["vehicle"]
        # Loops through each result
        for result in results:
            # Parses the year
            try:
                year = str(result["year"])
            except Exception:
                continue
            # Parses the price data
            try:
                price = str(round(result["price"]))
            except Exception:
                continue
            # Parses mileage
            try:
                miles = str(result["mileage"])
                if miles == None:
                    miles = "0"
            except Exception:
                continue
            # Puts data into CSV format
            data = year + "," + price + "," + miles
            # Writes the data to CSV file
            file.write(data)
            file.write("\n")
    file.close()
    print ("Done Scraping Cars.com!")

if __name__ == "__main__":
    # Creates a path
    path = Path("output/carsdotcom.csv")
    # Wipes the CSV file
    formatUtil.fileWipe(path)
    # Runs the scraper
    scraper(path)
