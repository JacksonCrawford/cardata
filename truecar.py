import requests
from bs4 import BeautifulSoup
from config import CarConfig
import linker

def scraper(url):
    # Opens the CSV file for data storage
    # Uses w+ mode; will create the csv file if it doesn't exist
    file = open("output/truecar.csv", "a")
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

# Main Method
if __name__ == "__main__":
    # Creates a config to grab info for the linker
    config = CarConfig()
    # Wipes the file
    with open("output/truecar.csv", "w") as f:
        f.close()
    # Loops through all of the links provided by the linker and scrapes each page
    for link in linker.truecar(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        scraper(link)
