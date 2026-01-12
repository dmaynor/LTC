Function DoubleEvens(Numbers() As Integer) As Collection
    Dim Result As New Collection
    Dim i As Integer
    For i = LBound(Numbers) To UBound(Numbers)
        If Numbers(i) Mod 2 = 0 Then
            Result.Add Numbers(i) * 2
        End If
    Next i
    Set DoubleEvens = Result
End Function
