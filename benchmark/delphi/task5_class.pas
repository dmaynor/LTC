unit PointUnit;

interface

type
  TPoint = class
  private
    FX, FY: Double;
  public
    constructor Create(X, Y: Double);
    function DistanceTo(Other: TPoint): Double;
    property X: Double read FX;
    property Y: Double read FY;
  end;

implementation

uses Math;

constructor TPoint.Create(X, Y: Double);
begin
  FX := X;
  FY := Y;
end;

function TPoint.DistanceTo(Other: TPoint): Double;
var
  DX, DY: Double;
begin
  DX := FX - Other.X;
  DY := FY - Other.Y;
  Result := Sqrt(DX * DX + DY * DY);
end;

end.
