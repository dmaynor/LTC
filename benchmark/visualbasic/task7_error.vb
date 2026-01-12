Module Parser
    Function ParseInt(s As String) As (Success As Boolean, Value As Integer, Error As String)
        Dim value As Integer
        If Integer.TryParse(s, value) Then
            Return (True, value, Nothing)
        End If
        Return (False, 0, "Invalid integer format")
    End Function
End Module
