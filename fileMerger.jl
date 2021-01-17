function wipeFile()
    open("master.csv", "w") do file
    end
end

function fileReader(fileName)
    open(fileName) do infile
        open("master.csv", "a") do outfile
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
    fileReader("truecar.csv")
    fileReader("cargurus.csv")
    fileReader("edmunds.csv")
end

main()
