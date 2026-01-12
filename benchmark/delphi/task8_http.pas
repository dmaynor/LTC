uses System.Net.HttpClient;

type
  TFetchResult = record
    Success: Boolean;
    Body: string;
  end;

function FetchUrl(const URL: string): TFetchResult;
var
  Client: THTTPClient;
  Response: IHTTPResponse;
begin
  Client := THTTPClient.Create;
  try
    try
      Response := Client.Get(URL);
      Result.Success := True;
      Result.Body := Response.ContentAsString;
    except
      on E: Exception do
      begin
        Result.Success := False;
        Result.Body := E.Message;
      end;
    end;
  finally
    Client.Free;
  end;
end;
