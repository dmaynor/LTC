import 'dart:io';

void countWords(String inputFile, String outputFile) {
  var text = File(inputFile).readAsStringSync();
  var counts = <String, int>{};

  for (var word in text.split(RegExp(r'\s+'))) {
    if (word.isNotEmpty) {
      counts[word] = (counts[word] ?? 0) + 1;
    }
  }

  var output = counts.entries.map((e) => '${e.key}: ${e.value}').join('\n');
  File(outputFile).writeAsStringSync(output);
}
