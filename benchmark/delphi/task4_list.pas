function DoubleEvens(const Numbers: array of Integer): TArray<Integer>;
var
  i, Count: Integer;
begin
  Count := 0;
  for i := Low(Numbers) to High(Numbers) do
    if Numbers[i] mod 2 = 0 then
      Inc(Count);

  SetLength(Result, Count);
  Count := 0;
  for i := Low(Numbers) to High(Numbers) do
    if Numbers[i] mod 2 = 0 then
    begin
      Result[Count] := Numbers[i] * 2;
      Inc(Count);
    end;
end;
