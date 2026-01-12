function double_evens(numbers)
    local result = {}
    for _, n in ipairs(numbers) do
        if n % 2 == 0 then
            table.insert(result, n * 2)
        end
    end
    return result
end
