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

    cards = soup.find_all(class_="d-flex mb-0_75 mb-md-1_5 col-12 col-md-6")
    for card in cards:
        year = str(card.find(class_="card-title size-16 text-primary-darker font-weight-bold d-block mb-0_5").contents[0])
        model = (card.find(class_="card-title size-16 text-primary-darker font-weight-bold d-block mb-0_5"))
        try:
            price = str((card.find(class_="display-price font-weight-bold text-gray-darker")).contents[0].replace(",", ""))
        except AttributeError:
            price = "No Price"
        try:
            trim = str(card.find(class_="card-title size-16 text-primary-darker font-weight-bold d-block mb-0_5").contents[0])
        except AttributeError:
            trim = "Not Listed"
        try:
            miles = str(card.find(class_="size-14").contents[0])
            miles = miles[miles.find("</svg>") + 6:miles.find("</div>"):]
            miles = miles.replace("<!-- -->", "").replace(",", "")
        except AttributeError:
            miles = "Not Listed"
        try:
            location = ""
            location += str(card.find(class_="size-14").contents[0])
        except AttributeError:
            location = "Not Listed"
        '''try:
            color = ""
            for y in range(1, 8):
                color += str(card.find(class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").contents[y])
            color = color.replace(",", "")
            color = color.replace("  ", " ")
        except AttributeError:
            color = "Not Listed"'''

        print(str(year) + " " + str(model) + ", " + str(price) + ", " + str(trim) + ", " + str(miles) + ", " + str(location))


edmunds()
