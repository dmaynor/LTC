procedure CountWords(const InputFile, OutputFile: string);
var
  Words: TStringList;
  Counts: TDictionary<string, Integer>;
  Word: string;
  Count: Integer;
  F: TextFile;
begin
  Words := TStringList.Create;
  Counts := TDictionary<string, Integer>.Create;
  try
    Words.LoadFromFile(InputFile);
    Words.Delimiter := ' ';
    Words.DelimitedText := Words.Text;

    for Word in Words do
    begin
      if Word <> '' then
      begin
        if Counts.TryGetValue(Word, Count) then
          Counts[Word] := Count + 1
        else
          Counts.Add(Word, 1);
      end;
    end;

    AssignFile(F, OutputFile);
    Rewrite(F);
    for Word in Counts.Keys do
      WriteLn(F, Word + ': ' + IntToStr(Counts[Word]));
    CloseFile(F);
  finally
    Words.Free;
    Counts.Free;
  end;
end;
