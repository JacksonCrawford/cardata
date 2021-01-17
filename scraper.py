import formatUtil
import truecar
import cargurus
import edmunds

# Runs all of the scrapers into master.csv
if __name__ == "__main__":
    # Wipes the file
    formatUtil.fileWipe("output/master.csv")
    # Activates all the scrapers
    truecar.scraper("output/master.csv")
    cargurus.scraper("output/master.csv")
    edmunds.scraper("output/master.csv")
