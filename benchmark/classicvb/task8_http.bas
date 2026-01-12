Function FetchUrl(Url As String) As Variant
    Dim Http As Object
    On Error GoTo ErrorHandler

    Set Http = CreateObject("MSXML2.XMLHTTP")
    Http.Open "GET", Url, False
    Http.Send

    FetchUrl = Array(True, Http.responseText)
    Exit Function

ErrorHandler:
    FetchUrl = Array(False, Err.Description)
End Function
