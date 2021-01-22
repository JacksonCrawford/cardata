using DataFrames, GLM
using Statistics
using Plots
using CSV
using IniFile
theme(:juno)

line = 0

function getData()
    data = CSV.read("output/master.csv", DataFrame)
    #print(data)
    return data
end

function plotData()
    data = getData()

    config = read(Inifile(),"config.ini")

    make = uppercase(string(get(config, "Search Criteria", "make", default)))
    model = uppercase(string(get(config, "Search Criteria", "model", default)))

    years = data.year
    prices = data.price
    mileage = data.mileage


    priceData = DataFrame(X=prices, Y=years)
    olsPrice = lm(@formula(X ~ Y), priceData)
    linearFitP = predict(olsPrice)

    mileData = DataFrame(X=mileage, Y=years)
    olsMiles = lm(@formula(X ~ Y), mileData)
    linearFitM = predict(olsMiles)


    plotlyjs()

    # Plotting Prices
    pricePlot = scatter(years, prices, title="Price of $make $model's",
        xlabel="Year", ylabel="Price", legend=true, label="Prices")
    plot!(years, linearFitP, label="linreg")

    # Plotting Mileage
    milePlot = scatter(years, mileage, title="Mileage of $make $model's",
        xlabel="Year", ylabel="Mileage", legend=false)
    plot!(years, linearFitM)

    linregPlot = plot(years, linearFitP, title="Linear Regression Compared",
        xlabel="Year", label = "price")
    plot!(years, linearFitM, label="mileage")

    # Plotting everything
    plot(pricePlot, milePlot, linregPlot, layout=grid(3,1), size=(650,800), legend=true)

end

function main()
    plotData()
end


main()
