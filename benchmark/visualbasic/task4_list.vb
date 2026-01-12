Imports System.Linq

Module ListOps
    Function DoubleEvens(numbers As List(Of Integer)) As List(Of Integer)
        Return numbers.Where(Function(n) n Mod 2 = 0).Select(Function(n) n * 2).ToList()
    End Function
End Module
