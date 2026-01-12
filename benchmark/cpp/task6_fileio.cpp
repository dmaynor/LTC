#include <fstream>
#include <sstream>
#include <map>
#include <string>

void count_words(const std::string& input_file, const std::string& output_file) {
    std::map<std::string, int> counts;
    std::ifstream in(input_file);
    std::string word;

    while (in >> word)
        counts[word]++;

    std::ofstream out(output_file);
    for (const auto& [w, c] : counts)
        out << w << ": " << c << "\n";
}
