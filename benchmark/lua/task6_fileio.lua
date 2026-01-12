function count_words(input_file, output_file)
    local counts = {}
    local file = io.open(input_file, "r")
    local text = file:read("*all")
    file:close()

    for word in text:gmatch("%S+") do
        counts[word] = (counts[word] or 0) + 1
    end

    file = io.open(output_file, "w")
    for word, count in pairs(counts) do
        file:write(word .. ": " .. count .. "\n")
    end
    file:close()
end
