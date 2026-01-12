Sub CountWords(InputFile As String, OutputFile As String)
    Dim FSO As Object, InFile As Object, OutFile As Object
    Dim Text As String, Words() As String
    Dim Counts As Object, Word As Variant

    Set FSO = CreateObject("Scripting.FileSystemObject")
    Set InFile = FSO.OpenTextFile(InputFile, 1)
    Text = InFile.ReadAll
    InFile.Close

    Words = Split(Text, " ")
    Set Counts = CreateObject("Scripting.Dictionary")

    For Each Word In Words
        If Counts.Exists(Word) Then
            Counts(Word) = Counts(Word) + 1
        Else
            Counts.Add Word, 1
        End If
    Next

    Set OutFile = FSO.CreateTextFile(OutputFile, True)
    For Each Word In Counts.Keys
        OutFile.WriteLine Word & ": " & Counts(Word)
    Next
    OutFile.Close
End Sub
