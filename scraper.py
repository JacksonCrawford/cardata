import formatUtil
import config
import truecar
import cargurus
import edmunds
import autotrader
import carsdotcom

# Runs all of the scrapers into master.csv
if __name__ == "__main__":
    # Prompts the user to change the config if they want
    config.CarConfig().promptConfigChange()
    # Stores the master CSV file path/name
    outputFilename = "output/master.csv"
    # Wipes the file
    formatUtil.fileWipe(outputFilename)
    # Activates all the scrapers
    truecar.scraper(outputFilename)
    cargurus.scraper(outputFilename)
    edmunds.scraper(outputFilename)
    autotrader.scraper(outputFilename)
    carsdotcom.scraper(outputFilename)
    # Checks for duplicate entries in the master.csv file
    formatUtil.removeDupe()
    print("Completely Finished!")
