Public Class Point
    Public Property X As Double
    Public Property Y As Double

    Public Sub New(x As Double, y As Double)
        Me.X = x
        Me.Y = y
    End Sub

    Public Function DistanceTo(other As Point) As Double
        Dim dx As Double = X - other.X
        Dim dy As Double = Y - other.Y
        Return Math.Sqrt(dx * dx + dy * dy)
    End Function
End Class
