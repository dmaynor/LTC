function count_words(input_file, output_file)
    text = read(input_file, String)
    words = split(text)
    counts = Dict{String, Int}()

    for word in words
        counts[word] = get(counts, word, 0) + 1
    end

    open(output_file, "w") do f
        for (word, count) in counts
            println(f, "$word: $count")
        end
    end
end
