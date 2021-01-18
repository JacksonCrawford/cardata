import formatUtil
import truecar
import cargurus
import edmunds
import autotrader

# Runs all of the scrapers into master.csv
if __name__ == "__main__":
    # Stores the master CSV file path/name
    outputFilename = "output/master.csv"
    # Wipes the file
    formatUtil.fileWipe(outputFilename)
    # Activates all the scrapers
    truecar.scraper(outputFilename)
    cargurus.scraper(outputFilename)
    edmunds.scraper(outputFilename)
    autotrader.scraper(outputFilename)
    # Checks for duplicate entries in the master.csv file
    formatUtil.removeDupe()
    print("Completely Finished!")
