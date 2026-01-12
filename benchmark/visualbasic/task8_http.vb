Imports System.Net.Http

Module HttpFetch
    Async Function FetchUrl(url As String) As Task(Of (Success As Boolean, Body As String))
        Try
            Using client As New HttpClient()
                Dim response = Await client.GetStringAsync(url)
                Return (True, response)
            End Using
        Catch ex As Exception
            Return (False, ex.Message)
        End Try
    End Function
End Module
