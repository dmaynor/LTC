const fs = require('fs');

function countWords(inputFile, outputFile) {
    const text = fs.readFileSync(inputFile, 'utf8');
    const counts = {};

    text.split(/\s+/).filter(w => w).forEach(word => {
        counts[word] = (counts[word] || 0) + 1;
    });

    const output = Object.entries(counts)
        .map(([word, count]) => `${word}: ${count}`)
        .join('\n');

    fs.writeFileSync(outputFile, output);
}
