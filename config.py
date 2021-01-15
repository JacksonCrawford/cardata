# A Configuration File Parser for the Car Website Scraper
#         _______
#        //  ||\ \
#  _____//___||_\ \___
#  )  _          _    \
#  |_/ \________/ \___|
# ___\_/________\_/______
import configparser
import os

class CarConfig:

    def __init__(self):
        # Opens the config file or creates it if it doesn't exist
        self.config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            self.config['Scrape Links'] = {'carGurus': '', 'autoTrader': '',
                                           'carsDotCom': '', 'trueCar': '', 'edmunds': '', 'carsDirect': ''}
            with open('config.ini', 'w+') as configfile:
                self.config.write(configfile)
            print("Please fill out the config file and restart the application!")
            exit()
        # Reads the config file for their values
        self.config.read('config.ini')
        # Stores read values into instance variables
        self._carGurusLink = self.config['Scrape Links']['carGurus']
        self._autoTraderLink = self.config['Scrape Links']['autoTrader']
        self._carsDotComLink = self.config['Scrape Links']['carsDotCom']
        self._trueCarLink = self.config['Scrape Links']['trueCar']
        self._edmundsLink = self.config['Scrape Links']['edmunds']
        self._carsDirectLink = self.config['Scrape Links']['carsDirect']

    def getCarGurusLink(self):
        # Get method for the link to Car Gurus
        return self._carGurusLink

    def getAutoTraderLink(self):
        # Get method for the link to AutoTrader
        return self._autoTraderLink

    def getCarsDotComLink(self):
        # Get method for the link to cars.com
        return self._carsDotComLink

    def getTrueCarLink(self):
        # Get method for the link to TrueCar
        return self._trueCarLink

    def getEdmundsLink(self):
        # Get method for the link to Edmunds
        return self._edmundsLink

    def getCarsDirectLink(self):
        # Get method for the link to Cars Direct
        return self._carsDirectLink
