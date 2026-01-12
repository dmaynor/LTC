Function ParseInt(S As String) As Variant
    On Error GoTo ErrorHandler
    ParseInt = Array(True, CInt(S), "")
    Exit Function
ErrorHandler:
    ParseInt = Array(False, 0, "Invalid integer format")
End Function
