import Foundation

func countWords(inputFile: String, outputFile: String) throws {
    let text = try String(contentsOfFile: inputFile)
    let words = text.split(separator: " ").map(String.init)
    var counts: [String: Int] = [:]

    for word in words {
        counts[word, default: 0] += 1
    }

    let output = counts.map { "\($0.key): \($0.value)" }.joined(separator: "\n")
    try output.write(toFile: outputFile, atomically: true, encoding: .utf8)
}
