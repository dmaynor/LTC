function count_words(input_file, output_file)
    text = fileread(input_file);
    words = split(text);
    [unique_words, ~, idx] = unique(words);
    counts = accumarray(idx, 1);

    fid = fopen(output_file, 'w');
    for i = 1:length(unique_words)
        fprintf(fid, '%s: %d\n', unique_words{i}, counts(i));
    end
    fclose(fid);
end
