#  DEPRACATED, DO NOT USE

function wipeFile()
    open("output/master.csv", "w") do file
    end
end

function fileReader(fileName)
    open(fileName) do infile
        open("output/master.csv", "a") do outfile
            line = 0
            data = ""
            while !eof(infile)
                #data = string(readline(f), ", ", data)
                write(outfile, readline(infile))
                write(outfile, "\n")
                line += 1
            end
            return data
        end
    end
end

function main()
    wipeFile()
    fileReader("output/truecar.csv")
    fileReader("output/cargurus.csv")
    fileReader("output/edmunds.csv")
end

main()
