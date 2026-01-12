from collections import Counter

def count_words(input_file, output_file):
    with open(input_file) as f:
        words = f.read().split()
    counts = Counter(words)
    with open(output_file, 'w') as f:
        for word, count in counts.items():
            f.write(f"{word}: {count}\n")
