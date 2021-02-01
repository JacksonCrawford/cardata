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
    for link in linker.edmunds(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        # Makes a request to the edmunds site for the source code
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        site = requests.get(link, headers=headers)
        # Converts the data to JSON for easy digestion
        jsonData = json.loads(site.text)
        # Grabs car results from json
        results = jsonData["inventories"]["results"]
        # Loops through each result
        for result in results:
            # Parses the year
            try:
                year = str(result["vehicleInfo"]["styleInfo"]["year"])
            except:
                continue
            # Parses the price data
            try:
                price = str(round(result["prices"]["displayPrice"]))
            except Exception:
                price = str(round(result["prices"]["baseMsrp"]))
            # Add a check for blank prices
            if (price == "0"):
                continue
            # Parses mileage
            try:
                miles = str(result["vehicleInfo"]["mileage"])
            except Exception:
                continue
            # Puts data into CSV format
            data = year + "," + price + "," + miles
            # Writes the data to CSV file
            file.write(data)
            file.write("\n")
    file.close()
    print ("Done Scraping Edmunds!")

if __name__ == "__main__":
    # Creates a path to the CSV file
    path = Path("output/edmunds.csv")
    # Wipes the CSV file
    formatUtil.fileWipe(path)
    # Runs the scraper
    scraper(path)
