using DataFrames, GLM
using Statistics
using Plots
theme(:juno)

line = 0

function getData()
    open("output/master.csv") do f
        data = ""
        while !eof(f)
            data = string(readline(f), ",", data)
            global line += 1
        end
        return data
    end
end

function plotData()
    data = getData()
    elements = line * 3


    years = Int64[]
    prices = Int64[]
    mileage = Int64[]
    cars = split(data, ",")

    # Creating an array of year/model
    for a in 1:3:elements
        year = cars[a]
        push!(years, parse(Int64, year))
    end

    # Creating an array of prices
    for b in 2:3:elements
        price = cars[b]
        if price != "No Price"
            price = parse(Int64, price)
        else
            price = 0
        end
        push!(prices, price)
    end

    # Creating an array of mileage
    for d in 3:3:elements
        miles = cars[d]
        if miles != "Not Listed"
            miles = parse(Int64, miles)
        else
            miles = 0
        end
        push!(mileage, miles)
    end

    yearDict = Dict()

    yearSet = Set(years)
    priceSet = Set(prices)
    mileageSet = Set(mileage)
    #=years = collect(yearSet)
    prices = collect(priceSet)
    mileage = collect(mileageSet)=#

    priceData = DataFrame(X=prices, Y=years)
    olsPrice = lm(@formula(X ~ Y), priceData)
    linearFitP = predict(olsPrice)

    meanPrices = Float64[]

    for year in years
        data = priceData[priceData.Y .== year, :X]
        mean = sum(data) / length(data)
        push!(meanPrices, mean)
    end

    mileData = DataFrame(X=mileage, Y=years)
    olsMiles = lm(@formula(X ~ Y), mileData)
    linearFitM = predict(olsMiles)

    meanMiles = Float64[]

    for year in years
        data = priceData[priceData.Y .== year, :X]
        mean = sum(data) / length(data)
        push!(meanMiles, mean)
    end

    #=for year in yearSet
        data = mileData[mileData.Y .== year, :X]
        mean = sum(data) / length(data)
        #println(mean)
    end=#


    plotlyjs()

    # Plotting Prices
    pricePlot = scatter(years, prices, title="Price of Porsche 911's",
        xlabel="Year", ylabel="Price", legend=true)
    plot!(years, linearFitP)
    scatter!(years, meanPrices)

    # Plotting Mileage
    milePlot = scatter(years, mileage, title="Mileage of Porsche 911's",
        xlabel="Year", ylabel="Mileage", legend=true)
    plot!(years, linearFitM)
    scatter!(years, meanMiles)

    # Plotting everything
    plot(pricePlot, milePlot, layout=grid(2,1), size=(650,800), legend=true)

end

function main()
    plotData()
end


main()
