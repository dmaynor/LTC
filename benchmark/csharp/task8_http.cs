using System.Net.Http;

async Task<(bool Success, string Body)> FetchUrl(string url)
{
    try
    {
        using var client = new HttpClient();
        var response = await client.GetStringAsync(url);
        return (true, response);
    }
    catch (Exception e)
    {
        return (false, e.Message);
    }
}
