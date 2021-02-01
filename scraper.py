import formatUtil
import config
import truecar
import cargurus
import edmunds
import autotrader
import carsdotcom
from pathlib import Path

# Runs all of the scrapers into master.csv
if __name__ == "__main__":
    # Prompts the user to change the config if they want
    config.CarConfig().promptConfigChange()
    # Stores the master CSV file path/name
    outputFile = Path("output/master.csv")
    # Wipes the file
    formatUtil.fileWipe(outputFile)
    # Adds headers
    formatUtil.addHeaders(outputFile)
    # Activates all the scrapers
    truecar.scraper(outputFile)
    cargurus.scraper(outputFile)
    edmunds.scraper(outputFile)
    autotrader.scraper(outputFile)
    carsdotcom.scraper(outputFile)
    # Checks for duplicate entries in the master.csv file
    formatUtil.removeDupe(outputFile)
    print("Completely Finished!")
