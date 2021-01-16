import requests
from bs4 import BeautifulSoup
import lxml

def truecar(make, model, city, state):
    # Use page 1 to get last number of pages
    link = "https://www.truecar.com/used-cars-for-sale/listings/" + make + "/" + model + "/location-" + city + "-" + state + "/?page=1&sort[]=best_match"
    site = requests.get(link)
    soup = BeautifulSoup(site.text, "lxml")
    alphaSoup = soup.find_all(class_="page-link")
    nums = list()
    num = int()

    for link in alphaSoup:
        if len(str(link.contents[0])) <= 2:
            nums.append(link.contents[0])
    try:
        num = int(nums[-1])
    except TypeError:
        print("banana")
    except IndexError:
        return [link]

    # Use number of pages to create a list of links for every page number
    linkList = list()
    for number in range(num):
        linkList.append("https://www.truecar.com/used-cars-for-sale/listings/" + make + "/" + model + "/location-" + city + "-" + state + "/?page=" + str(num) + "&sort[]=best_match")
        num -= 1

    return linkList
