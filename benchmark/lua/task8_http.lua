local http = require("socket.http")

function fetch_url(url)
    local body, code = http.request(url)
    if code == 200 then
        return {success = true, body = body}
    end
    return {success = false, error = "HTTP error: " .. tostring(code)}
end
