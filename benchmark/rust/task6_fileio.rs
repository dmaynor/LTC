use std::collections::HashMap;
use std::fs;
use std::io::Write;

fn count_words(input_file: &str, output_file: &str) -> std::io::Result<()> {
    let text = fs::read_to_string(input_file)?;
    let mut counts: HashMap<&str, usize> = HashMap::new();

    for word in text.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }

    let mut file = fs::File::create(output_file)?;
    for (word, count) in &counts {
        writeln!(file, "{}: {}", word, count)?;
    }
    Ok(())
}
