# Utility functions for formatting scraped car data

def createYMMString(year, make, model):
    # @param year - an integer for the year of the car (ex. 2021)
    # @param make - a string saying which company made the car (ex. "Porsche")
    # @param model - a string saying what model the car is (ex. "Macan")
    if year and make and model:
        return str(year) + " " + make + " " + model
    else:
        return "Something Is Definitely Wrong! D:"

def createLocationString(distance, city):
    # @param distance - an integer of the distance to the car (in miles, ex. 48.93)
    # @param city - a string of the city where the car is located (ex. "Charlotte")
    if distance and city:
        return str(round(distance)) + " mi - " + city
    else:
        return "Not Listed"

def createColorString(exteriorColor, interiorColor):
    # @param exteriorColor - a string of a normalized exterior color (ex. "White") 
    # @param interiorColor - a string of a normalized interior color (ex. "Black") 
    if exteriorColor and interiorColor:
        # Normalizes the colors to have the first letter capitalized and the rest lowercase
        # Ex. Turns "WHITE" into "White"
        normalizedExterior = exteriorColor[0].upper() + exteriorColor[1:].lower()
        normalizedInterior = interiorColor[0].upper() + interiorColor[1:].lower()
        # Returns the concatenated string format
        return normalizedExterior + " exterior " + normalizedInterior + " interior"
    else:
        return "Not Listed"