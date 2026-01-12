def count_words(input_file, output_file)
  text = File.read(input_file)
  counts = Hash.new(0)
  text.split.each { |word| counts[word] += 1 }

  File.open(output_file, 'w') do |f|
    counts.each { |word, count| f.puts "#{word}: #{count}" }
  end
end
