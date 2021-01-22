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

    def promptConfigChange(self):
        # Allows the user to change the config in the terminal before running the scrapers
        print("\nCarData Scraper by Jackson C. and Mitch Z.")
        print("Input New Config Values Below. Press Enter/Return To Use The Current Config Value.\n")
        # Grabs the make or uses the current make if nothing is inputted
        print("Car Make (ex. Toyota): ", end="")
        make = input()
        if (len(make) == 0):
            make = self.getMake()
        # Grabs the model or uses the current model if nothing is inputted
        print("Car Model (ex. Camry): ", end="")
        model = input()
        if (len(model) == 0):
            model = self.getModel()
        # Grabs the city or uses the current city if nothing is inputted
        print("City (ex. Charlotte): ", end="")
        city = input()
        if (len(city) == 0):
            city = self.getCity()
        # Grabs the state code or uses the current state if nothing is inputted
        print("State Code (ex. NC): ", end="")
        state = input()
        if (len(state) == 0):
            state = self.getState()
        print("\n", end="")
        # Puts the new values into the config object
        self.config['Search Criteria'] = {'make': make, 'model': model,
                                          'city': city, 'stateCode': state}
        # Writes the values to the config file
        with open('config.ini', 'w+') as configFile:
            self.config.write(configFile)

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
