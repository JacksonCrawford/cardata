# cardata
Program for finding used cars across various sites and calculating price and mileage data.

## Project Overview
***

The collection of programs work in unison in order to scrape used car sites, report the listing to the user, and calculate useful data such as price-related statistics. The following sites will be scraped:

- [CarGurus](https://www.cargurus.com/)
- [Autotrader](https://www.autotrader.com/)
- [Cars.com](https://www.cars.com/)
- [TrueCar](https://www.truecar.com/)
- [Edmunds](https://www.edmunds.com/)
- [CarsDirect](https://www.carsdirect.com/)

### Requirements
***

A number of these libraries and packages will likely come installed on most systems, but in order to ensure that you have all of them, it is easiest to try and install all of these.

Python libraries can be easily installed by using pip:

```pip3 install [LibraryName]```

Julia packages require an extra step, and you must be in the Julia REPL to perform the following:

```using Pkg```
then,
```Pkg.add("[PackageName]")```

The library and package names are included in the list below in the parentheses, and they are case-sensitive!

- [Python](https://www.python.org)
  - [BeatifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) (BeautifulSoup4)
  - [lxml](https://lxml.de/) (lxml)
  - [requests](https://requests.readthedocs.io/en/master/) (requests)
  - [selenium](https://pythonspot.com/selenium/) (selenium)
  - [more-itertools](https://pypi.org/project/more-itertools/)
- [Julia](https://www.julialang.org)
  - [Plots](http://docs.juliaplots.org/latest/) (Plots)
  - [PlotlyJS](https://juliapackages.com/p/plotlyjs) (PlotlyJS)
  - [GLM](https://juliapackages.com/p/glm) (GLM)
  - [DataFrames](https://juliapackages.com/p/dataframes)
  - [CSV](https://juliapackages.com/p/csv)
  - [IniFile](https://juliapackages.com/p/inifile)
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
