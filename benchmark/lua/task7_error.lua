function parse_int(s)
    local n = tonumber(s)
    if n and math.floor(n) == n then
        return {success = true, value = n}
    end
    return {success = false, error = "Invalid integer format"}
end
