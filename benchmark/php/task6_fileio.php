<?php
function count_words(string $inputFile, string $outputFile): void {
    $text = file_get_contents($inputFile);
    $words = preg_split('/\s+/', $text, -1, PREG_SPLIT_NO_EMPTY);
    $counts = array_count_values($words);

    $output = '';
    foreach ($counts as $word => $count) {
        $output .= "$word: $count\n";
    }
    file_put_contents($outputFile, $output);
}
