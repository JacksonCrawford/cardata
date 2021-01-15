using Plots

function getData()
    open("truecar.csv") do f
        data = ""
        line = 0
        while !eof(f)
            data = string(readline(f), ", ", data)
            line += 1
        end
        return data
    end
end

function plotData()
    data = getData()
    years = []
    prices = []
    cars = split(data, ", ")

    # Creating an array of year/model
    for a in 1:6:102
        year = cars[a]
        push!(years, parse(Int64, year[1:4]))
        #println(year[1:4])
    end

    # Creating an array of prices
    for b in 2:6:102
        price = replace(cars[b], "," =>"")
        if price != "No Price"
            price = parse(Int64, price[2:end])
        else
            price = 0
        end
        push!(prices, price)
    end

    # Plotting Prices
    gr()

    scatter(years, prices, label="points", legend=false)

    title!("Price of Porsche 911's (TrueCar)")
    xlabel!("Year")
    ylabel!("Price")

end

function main()
    plotData()
end

main()
