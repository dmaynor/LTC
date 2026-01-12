with Ada.Numerics.Elementary_Functions; use Ada.Numerics.Elementary_Functions;

package body Point_Pkg is
   function Create(X, Y : Float) return Point is
   begin
      return (X => X, Y => Y);
   end Create;

   function Distance_To(Self, Other : Point) return Float is
      DX : Float := Self.X - Other.X;
      DY : Float := Self.Y - Other.Y;
   begin
      return Sqrt(DX * DX + DY * DY);
   end Distance_To;
end Point_Pkg;
