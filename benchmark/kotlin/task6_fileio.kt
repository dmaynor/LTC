import java.io.File

fun countWords(inputFile: String, outputFile: String) {
    val counts = File(inputFile).readText()
        .split(Regex("\\s+"))
        .filter { it.isNotEmpty() }
        .groupingBy { it }
        .eachCount()

    File(outputFile).writeText(counts.entries.joinToString("\n") { "${it.key}: ${it.value}" })
}
