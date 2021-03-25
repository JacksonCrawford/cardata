using DataFrames, GLM, Statistics
using Plots
using CSV, IniFile

# Function that uses the CSV package to read master.csv and store it as a DataFrame
function getData()
    data = CSV.read("output/master.csv", DataFrame)
    return data
end

# Functin that plots the data from master.csv
function plotData()
    # Calls getData and stores master.csv DataFrame in variable "data"
    data = getData()

    # Reads config.ini and stores it in variable "config"
    config = read(Inifile(),"config.ini")

    #= Takes make, model, city, and state values from config.ini and stores them
        in their respective variables =#
    make = uppercase(string(get(config, "Search Criteria", "make", default)))
    model = uppercase(string(get(config, "Search Criteria", "model", default)))
    city = uppercase(string(get(config, "Search Criteria", "city", default)))
    state = uppercase(string(get(config, "Search Criteria", "statecode", default)))

    #= Gets year, price, and mileage data from respective columns in "data" DataFrame
        and stores them in Array variables =#
    years = data.year
    prices = data.price
    mileage = data.mileage

    # Creates a DataFrame of prices and years
    priceData = DataFrame(X=prices, Y=years)
    # Calculates Ordinary Least Squared data for prices
    olsPrice = lm(@formula(X ~ Y), priceData)
    # Uses olsPrices to calculate linear regression
    linearFitP = predict(olsPrice)

    # Creates a DataFrame of mileage and years
    mileData = DataFrame(X=mileage, Y=years)
    # Calculates Ordinary Least Squared data for mileage
    olsMiles = lm(@formula(X ~ Y), mileData)
    # Uses olsMiles to calculate linear regression
    linearFitM = predict(olsMiles)

    # Creates a DataFrame of prices and mileage
    ratioData = DataFrame(X=mileage, Y=prices)
    # Calculates Ordinary Least Squared data for price-mileage ratio
    olsRatio = lm(@formula(X ~ Y), ratioData)
    # Uses olsRatio to calculate linear regression
    linearFitR = predict(olsRatio)

    #= Uses PlotlyJS backend with juno theme. Other themes can be found here:
        http://docs.juliaplots.org/latest/generated/plotthemes/. Other backends
        can be used as well, such as gr(), though they do not all have the same
        interactive abilities as PlotlyJS =#
    plotlyjs()
    theme(:juno)

    # Plotting Prices (scatter)
    pricePlot = scatter(years, prices, title="Price of $make $model's in $city, $state",
        xlabel="Year", ylabel="Price", legend=true, label="Prices")
    # Plotting linear regression line on scatter plot
    plot!(years, linearFitP, label="linreg")

    # Plotting Mileage (scatter)
    milePlot = scatter(years, mileage, title="Mileage of $make $model's in $city, $state",
        xlabel="Year", ylabel="Mileage", legend=false)
    # Plotting linear regression line on scatter plot
    plot!(years, linearFitM)

    # Plotting both linreg's together (WIP)
    ratioPlot = scatter(prices, mileage, title="Price to Mileage ratio",
        xlabel = "Price", ylabel="Mileage", legend=false)
    # Plotting linear regression line on scatter plot
    plot!(prices, linearFitR)

    # Plotting everything
    plot(pricePlot, milePlot, ratioPlot, layout=grid(3,1), size=(675,950), legend=false)
end

# Main function
function main()
    plotData()
end

main()
