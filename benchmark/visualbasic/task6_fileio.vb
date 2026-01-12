Imports System.IO
Imports System.Linq

Module WordCount
    Sub CountWords(inputFile As String, outputFile As String)
        Dim counts = File.ReadAllText(inputFile) _
            .Split() _
            .Where(Function(w) Not String.IsNullOrEmpty(w)) _
            .GroupBy(Function(w) w) _
            .ToDictionary(Function(g) g.Key, Function(g) g.Count())

        File.WriteAllLines(outputFile, counts.Select(Function(kv) $"{kv.Key}: {kv.Value}"))
    End Sub
End Module
