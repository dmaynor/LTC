Sub FizzBuzz()
    Dim i As Integer
    For i = 1 To 100
        If i Mod 15 = 0 Then
            Debug.Print "FizzBuzz"
        ElseIf i Mod 3 = 0 Then
            Debug.Print "Fizz"
        ElseIf i Mod 5 = 0 Then
            Debug.Print "Buzz"
        Else
            Debug.Print i
        End If
    Next i
End Sub
