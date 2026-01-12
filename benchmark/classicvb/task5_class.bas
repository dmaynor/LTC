' Point.cls
Public X As Double
Public Y As Double

Public Function DistanceTo(Other As Point) As Double
    Dim DX As Double, DY As Double
    DX = X - Other.X
    DY = Y - Other.Y
    DistanceTo = Sqr(DX * DX + DY * DY)
End Function
