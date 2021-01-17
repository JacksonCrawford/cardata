from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

def getSource(url):
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html

def edmunds():
    soup = BeautifulSoup(getSource("https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&make=porsche&model=911"), "lxml")
    edmundSoup = soup.find("usurp-card-list list-unstyled align-items-stretch row")

    outfile = open("edmunds.csv", "w+")
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

edmunds()
