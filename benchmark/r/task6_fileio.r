count_words <- function(input_file, output_file) {
  text <- readLines(input_file)
  words <- unlist(strsplit(text, "\\s+"))
  counts <- table(words)
  output <- paste(names(counts), counts, sep = ": ")
  writeLines(output, output_file)
}
