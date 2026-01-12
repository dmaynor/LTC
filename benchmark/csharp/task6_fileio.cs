using System.IO;
using System.Linq;

void CountWords(string inputFile, string outputFile)
{
    var counts = File.ReadAllText(inputFile)
        .Split()
        .Where(w => !string.IsNullOrEmpty(w))
        .GroupBy(w => w)
        .ToDictionary(g => g.Key, g => g.Count());

    File.WriteAllLines(outputFile, counts.Select(kv => $"{kv.Key}: {kv.Value}"));
}
