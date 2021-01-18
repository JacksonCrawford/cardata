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
            self.config['Search Criteria'] = {'make': '', 'model': '',
                                           'city': '', 'stateCode': ''}
            with open('config.ini', 'w+') as configfile:
                self.config.write(configfile)
            print("Please fill out the config file and restart the application!")
            exit()
        # Reads the config file for their values
        self.config.read('config.ini')
        # Stores read values into instance variables
        self._make = self.config['Search Criteria']['make']
        self._model = self.config['Search Criteria']['model']
        self._city = self.config['Search Criteria']['city']
        self._state = self.config['Search Criteria']['stateCode']

    def getMake(self):
        # Get method for the link to Car Gurus
        return self._make.lower()

    def getModel(self):
        # Get method for the link to AutoTrader
        return self._model.lower()

    def getCity(self):
        # Get method for the link to cars.com
        return self._city.lower()

    def getState(self):
        # Get method for the link to TrueCar
        return self._state.lower()

