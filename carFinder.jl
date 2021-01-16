using Plots
theme(:juno)

line = 0

function getData()
    open("master.csv") do f
        data = ""
        while !eof(f)
            data = string(readline(f), ", ", data)
            global line += 1
        end
        return data
    end
end

function plotData()
    data = getData()
    elements = line * 6

    years = []
    prices = []
    mileage = []
    locations = []
    cars = split(data, ", ")

    # Creating an array of year/model
    for a in 1:6:elements
        year = cars[a]
        push!(years, parse(Int64, year[1:4]))
    end

    # Creating an array of prices
    for b in 2:6:elements
        #price = replace(cars[b], "," =>"")
        price = cars[b]
        if price != "No Price"
            price = parse(Int64, price[2:end])
        else
            price = 0
        end
        push!(prices, price)
    end

    # Creating an array of mileage
    for d in 4:6:elements
        miles = cars[d]
        #miles = replace(cars[d], "," =>"")
        if miles != "Not Listed"
            miles = replace(miles, " miles" =>"")
            miles = parse(Int64, miles)
        else
            miles = 0
        end
        push!(mileage, miles)
    end

    for e in 5:6:elements
        location = cars[e]
        locationDex = findfirst(" mi", location)
        if location != "Not Listed"
            location = location[1:locationDex[1]]
            location = parse(Float64, location)
        else
            location = 0
        end
        push!(locations, location)
    end

    gr()

    # Plotting Prices
    pricePlot = scatter(years, prices, title="Price of Porsche 911's (TrueCar)",
        xlabel="Year", ylabel="Price", legend=false)

    # Plotting Mileage
    milePlot = scatter(years, mileage, title="Mileage of Porsche 911's (TrueCar)",
        xlabel="Year", ylabel="Mileage", legend=false)

    # Plotting Location
    locPlot = scatter(years, locations, title="Location of Porsche 911's (TrueCar)",
        xlabel="Year", ylabel="Miles from zip", legend=false)

    # Plotting everything
    plot(pricePlot, milePlot, locPlot, layout=grid(3,1), size=(650,800), legend=false)
end

function main()
    plotData()
end


main()
