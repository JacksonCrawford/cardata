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
    '''truecar.scraper("output/truecar.csv")
    formatUtil.removeDupe("output/truecar.csv")
    cargurus.scraper("output/cargurus.csv")
    formatUtil.removeDupe("output/cargurus.csv")
    edmunds.scraper("output/edmunds.csv")
    formatUtil.removeDupe("output/edmunds.csv")
    autotrader.scraper("output/autotrader.csv")
    formatUtil.removeDupe("output/autotrader.csv")'''
    truecar.scraper(outputFilename)
    cargurus.scraper(outputFilename)
    edmunds.scraper(outputFilename)
    autotrader.scraper(outputFilename)
    formatUtil.removeDupe()
    print("Completely Finished!")
