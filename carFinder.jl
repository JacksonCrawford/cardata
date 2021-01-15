#using Plots

function getData()
    open("truecar.csv") do f
        line = 0
        while !eof(f)
            s = readline(f)
            line += 1
            println(s)
        end
    end

end


#=function plotData()

end

function main()

end=#

getData()
