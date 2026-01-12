#include <string>
#include <variant>
#include <stdexcept>

struct ParseResult {
    bool success;
    int value;
    std::string error;
};

ParseResult parse_int(const std::string& s) {
    try {
        return {true, std::stoi(s), ""};
    } catch (const std::exception& e) {
        return {false, 0, e.what()};
    }
}
