using HTTP

function fetch_url(url)
    try
        response = HTTP.get(url)
        return (true, String(response.body))
    catch e
        return (false, string(e))
    end
end
