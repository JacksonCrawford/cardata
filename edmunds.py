from bs4 import BeautifulSoup
import requests
import formatUtil
import linker
from config import CarConfig

def getSource(url):
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html

def scraper(fileName):
    # Creates a CarConfig object for search criteria
    config = CarConfig()
    # Opens the CSV file for appending, will likely be wiped already
    file = open(fileName, "a")
    # Loops through each link provided by the linker and scrapes the site
    for link in linker.edmunds(config.getMake(), config.getModel(), config.getCity(), config.getState()):
        # Makes a request to the edmunds site for the source code
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        site = requests.get("https://www.edmunds.com/used-toyota-camry/", headers=headers)
        # Digests the source code using lxml and bs4
        soup = BeautifulSoup(site.text, "lxml")
        edmundSoup = soup.find("usurp-card-list list-unstyled align-items-stretch row")
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
            # print(data)
            file.write(data)
            file.write("\n")
    file.close()
    print ("Done Scraping Edmunds!")


if __name__ == "__main__":
    # Wipes the CSV file
    formatUtil.fileWipe("output/edmunds.csv")
    # Runs the scraper
    scraper("output/edmunds.csv")
