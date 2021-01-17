using Plots
theme(:juno)

line = 0

function getData()
    open("master.csv") do f
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

    years = []
    prices = []
    mileage = []
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

    gr()

    # Plotting Prices
    pricePlot = scatter(years, prices, title="Price of Porsche 911's (TrueCar)",
        xlabel="Year", ylabel="Price", legend=false)

    # Plotting Mileage
    milePlot = scatter(years, mileage, title="Mileage of Porsche 911's (TrueCar)",
        xlabel="Year", ylabel="Mileage", legend=false)

    # Plotting everything
    plot(pricePlot, milePlot, layout=grid(2,1), size=(650,800), legend=false)
end

function main()
    plotData()
end


main()
