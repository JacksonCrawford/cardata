import requests
from bs4 import BeautifulSoup, NavigableString
from config import CarConfig
import linker
import formatUtil
from pathlib import Path

def scraper(fileName):
    # Opens the CSV file for data storage
    # Uses w+ mode; will create the csv file if it doesn't exist
    file = open(fileName, "a")
    # Creates a config to grab info for the linker
    config = CarConfig()
    for link in linker.autotrader(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        # Creates a GET request to the autotrader link in the config
        site = requests.get(link)
        soup = BeautifulSoup(site.text, "lxml")
        creamySoup = soup.find(class_="col-xs-12 col-md-9")
        # Finds all of the car info cards on the website
        cards = creamySoup.find_all(class_="item-card row display-flex align-items-stretch flex-column")
        # Loops through all of the info cards to gather data
        for card in cards:
            # Quickly grabs the year of the car
            year = card.find(class_="text-bold text-size-400 text-size-sm-500 link-unstyled").contents[0].split(" ")[1]
            # Grabs the price of the car
            try:
                # Checks if there is a layered secondary price
                # New cars listed on autotrader have prices listed differently
                price = (card.find(class_="first-price")).contents[0]
                if type(price) == NavigableString:
                    price = price.replace(",", "")
                else:
                    price = price.find(class_="text-bold").contents[0].replace(",", "")
            except AttributeError:
                continue
            # Finds the mileage of the car
            try:
                miles = card.find(class_="item-card-specifications")
                miles = miles.find("div")
                miles = miles.contents[0].replace(" miles", "").replace(",", "")
            except AttributeError:
                continue
            # Formats the data into CSV format and writes it to the file
            data = year + "," + price + "," + miles
            file.write(data)
            file.write("\n")
    # Closes the CSV file after adding scraped data
    file.close()
    print("Done Scraping AutoTrader!")

# Main Method
if __name__ == "__main__":
    # Creates a file path
    path = Path("output/autotrader.csv")
    # Wipes the file
    formatUtil.fileWipe(path)
    # Runs the scraper
    scraper(path)
