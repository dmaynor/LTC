with AWS.Client;
with AWS.Response;

function Fetch_URL(URL : String) return Fetch_Result is
   Response : AWS.Response.Data;
begin
   Response := AWS.Client.Get(URL);
   return (Success => True, Body => AWS.Response.Message_Body(Response));
exception
   when others =>
      return (Success => False, Body => "Failed to fetch URL");
end Fetch_URL;
