function parse_int(s)
    try
        return (true, parse(Int, s), nothing)
    catch e
        return (false, 0, string(e))
    end
end
