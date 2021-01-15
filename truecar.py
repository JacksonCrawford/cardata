import requests
from bs4 import BeautifulSoup

file = open("truecar.csv", "w")

def scraper():
    site = requests.get("https://www.truecar.com/used-cars-for-sale/listings/porsche/911/location-charlotte-nc/")
    soup = BeautifulSoup(site.text, "lxml")
    creamySoup = soup.find(class_="row row-2 margin-bottom-3")

    cards = creamySoup.find_all(class_="card-content vehicle-card-body")
    for card in cards:
        year = card.find(class_="vehicle-card-year font-size-1").contents[0]
        model = card.find(class_="vehicle-header-make-model text-truncate")
        model = model.contents[0] + " " + model.contents[4]
        try:
            price = (card.find(class_="heading-3 margin-y-1 font-weight-bold")).contents[0]
        except AttributeError:
            price = "No Price"
        try:
            trim = card.find(class_="font-size-1 text-truncate").contents[0]
        except AttributeError:
            trim = "Not Listed"
        try:
            miles = str(card.find(class_="d-flex w-100 justify-content-between").contents[0])
            miles = miles[miles.find("</svg>") + 6:miles.find("</div>"):]
            miles = miles.replace("<!-- -->", "")
        except AttributeError:
            miles = "Not Listed"
        try:
            location = ""
            for x in range(1, 4):
                location += str(card.find(class_="vehicle-card-location font-size-1 margin-top-1").contents[x])
        except AttributeError:
            location = "Not Listed"
        try:
            color = ""
            for y in range(1, 8):
                color += str(card.find(class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").contents[y])
            color = color.replace(",", "")
            color = color.replace("  ", " ")
        except AttributeError:
            color = "Not Listed"

        print(year + " " + model + ", " + price + ", " + trim + ", " + miles + ", " + location + ", " + color)

        data = year + " " + model + ", " + price + ", " + trim + ", " + miles + ", " + location + ", " + color
        file.write(data)
        file.write("\n")




scraper()
file.close()
