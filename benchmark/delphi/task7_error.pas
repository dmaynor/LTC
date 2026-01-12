type
  TParseResult = record
    Success: Boolean;
    Value: Integer;
    Error: string;
  end;

function ParseInt(const S: string): TParseResult;
var
  Code: Integer;
begin
  Val(S, Result.Value, Code);
  Result.Success := Code = 0;
  if not Result.Success then
    Result.Error := 'Invalid integer format';
end;
